"""
Start passive real-time CICFlowMeter capture and send each flow to the local IDS API.

CICFlowMeter performs bidirectional flow feature extraction from live packets.
It is passive: this script only starts capture and sends extracted flow records
to the application's /api/predict-flow endpoint.
"""
import argparse
import subprocess
import sys

def main():
    parser = argparse.ArgumentParser(description="Run live CICFlowMeter -> Cyber Alert ML pipeline")
    parser.add_argument("--interface", "-i", required=True, help="Network interface to monitor")
    parser.add_argument("--url", default="http://127.0.0.1:8000/api/predict-flow")
    args = parser.parse_args()

    command = [
        "cicflowmeter",
        "-i", args.interface,
        "-u", args.url,
    ]
    print("Starting passive flow capture:", " ".join(command))
    print("Stop with Ctrl+C.")
    try:
        return subprocess.call(command)
    except FileNotFoundError:
        print("cicflowmeter is not installed. Run: pip install -r requirements.txt", file=sys.stderr)
        return 1

if __name__ == "__main__":
    raise SystemExit(main())
