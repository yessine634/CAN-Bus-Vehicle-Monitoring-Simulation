"""Local dashboard. Run with the project's .venv Python; no extra packages needed."""
import csv
import io
import json
import os
from pathlib import Path
import subprocess
import sys
import threading
import time
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
RUNTIME = ROOT / '.runtime'
for directory in (RUNTIME / 'tmp', RUNTIME / 'matplotlib'):
    directory.mkdir(parents=True, exist_ok=True)
os.environ.update(TEMP=str(RUNTIME / 'tmp'), TMP=str(RUNTIME / 'tmp'),
                  MPLCONFIGDIR=str(RUNTIME / 'matplotlib'), MPLBACKEND='Agg', PYTHONUTF8='1')
FIELDS = ('speed', 'rpm', 'engine_temp', 'battery_voltage', 'battery_current', 'battery_temp', 'brake_status')


class Simulation:
    def __init__(self):
        self.lock = threading.Lock()
        self.process = None
        self.started = None
        self.finished = None
        self.duration = 15
        self.stopping = False
        self.log = None
        self.stop_file = RUNTIME / 'stop-request'

    def start(self, duration):
        with self.lock:
            if self.process and self.process.poll() is None:
                raise ValueError('A simulation is already running.')
            if type(duration) is not int or not 5 <= duration <= 300:
                raise ValueError('Choose a duration between 5 and 300 seconds.')
            self.stop_file.unlink(missing_ok=True)
            if self.log:
                self.log.close()
            self.log = (RUNTIME / 'web-simulation.log').open('w', encoding='utf-8')
            self.started = time.time()
            self.finished = None
            self.duration = duration
            self.stopping = False
            self.process = subprocess.Popen(
                [sys.executable, '-u', str(ROOT / 'src' / 'main.py'), '--duration', str(duration),
                 '--stop-file', str(self.stop_file)], cwd=ROOT, stdout=self.log,
                stderr=subprocess.STDOUT, env=os.environ.copy(),
                creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))

    def stop(self):
        with self.lock:
            if self.process and self.process.poll() is None:
                self.stopping = True
                self.stop_file.touch()

    def snapshot(self):
        with self.lock:
            code = self.process.poll() if self.process else None
            running = bool(self.process and code is None)
            if self.process and not running and self.finished is None:
                self.finished = time.time()
            elapsed = min((self.finished or time.time()) - self.started, self.duration) if self.started else 0
            status = ('stopping' if self.stopping else 'running') if running else (
                'error' if self.process and code else 'completed' if self.process else 'idle')
            rows = []
            path = ROOT / 'data' / 'can_log.csv'
            if self.started and path.exists() and path.stat().st_mtime >= self.started - 0.01:
                try:
                    content = path.read_text(encoding='utf-8')
                    # Ignore a partially written final row while the logger is active.
                    content = content[:content.rfind('\n') + 1]
                    rows = list(csv.DictReader(io.StringIO(content)))
                except (OSError, csv.Error):
                    pass
            latest, history, faults, counts = {}, {field: [] for field in FIELDS}, [], {}
            for row in rows:
                for field in FIELDS:
                    try:
                        value = float(row.get(field, ''))
                    except (ValueError, TypeError):
                        continue
                    latest[field] = value
                    history[field].append(value)
                if row.get('fault_code'):
                    faults.append({key: row.get(key, '') for key in ('timestamp', 'fault_code', 'priority', 'message')})
                    counts[row['fault_code']] = counts.get(row['fault_code'], 0) + 1
            plots = []
            if status == 'completed':
                plots = [p.name for p in sorted((ROOT / 'plots').glob('*.png')) if p.stat().st_mtime >= self.started]
            log = RUNTIME / 'web-simulation.log'
            output = log.read_text(encoding='utf-8', errors='replace')[-18000:] if log.exists() and self.started else ''
            return dict(status=status, elapsed=round(elapsed, 1), duration=self.duration,
                        latest=latest, history=history, faults=faults[-100:][::-1],
                        fault_count=len(faults), counts=counts, rows=len(rows), plots=plots,
                        output=output, run_id=self.started)


simulation = Simulation()


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT / 'web'), **kwargs)

    def log_message(self, *args):
        pass

    def json_response(self, payload, code=200):
        data = json.dumps(payload).encode()
        self.send_response(code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Cache-Control', 'no-store')
        self.send_header('Content-Length', str(len(data)))
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self):
        path = urlparse(self.path).path
        if path == '/api/state':
            return self.json_response(simulation.snapshot())
        if path == '/api/download' or path.startswith('/plots/'):
            target = ROOT / 'data' / 'can_log.csv' if path == '/api/download' else ROOT / 'plots' / Path(path).name
            if not target.is_file() or (path != '/api/download' and target.suffix != '.png'):
                return self.send_error(404)
            content = target.read_bytes()
            self.send_response(200)
            self.send_header('Content-Type', 'text/csv' if target.suffix == '.csv' else 'image/png')
            if target.suffix == '.csv':
                self.send_header('Content-Disposition', 'attachment; filename="can_log.csv"')
            self.send_header('Content-Length', str(len(content)))
            self.end_headers()
            self.wfile.write(content)
            return
        return super().do_GET()

    def do_POST(self):
        if self.headers.get('X-Dashboard') != '1':
            return self.json_response({'error': 'Dashboard requests only.'}, 403)
        try:
            size = int(self.headers.get('Content-Length', '0'))
            if not 0 <= size <= 1024:
                raise ValueError('Invalid request size.')
            payload = json.loads(self.rfile.read(size) or b'{}')
            if self.path == '/api/start':
                simulation.start(payload.get('duration', 15))
            elif self.path == '/api/stop':
                simulation.stop()
            else:
                return self.send_error(404)
            return self.json_response({'ok': True})
        except (ValueError, TypeError, AttributeError) as error:
            return self.json_response({'error': str(error)}, 400)


if __name__ == '__main__':
    server = ThreadingHTTPServer(('127.0.0.1', 8000), Handler)
    print('Vehicle dashboard: http://127.0.0.1:8000', flush=True)
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        simulation.stop()
        if simulation.process and simulation.process.poll() is None:
            simulation.process.wait(timeout=30)
        server.server_close()
