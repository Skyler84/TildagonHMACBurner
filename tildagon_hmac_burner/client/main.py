#!/usr/bin/python

import hashlib
import esptool, espefuse
import os, hmac, time
import argparse

from ..common.master_secret import check_master_secret
from .device import ESP

LOADING_CHARS = ['|', '/', '-', '\\']

def port_matches(port: str, ports: set[str]) -> bool:
    if port in ports:
        return True
    if any([p[-1] == '*' and port.startswith(p[:-1]) for p in ports]):
        return True
    return False

def main(args: list[str]):
    parser = argparse.ArgumentParser(description="Burn HMAC key to device")
    parser.add_argument("--key", type=int, default=1, help="Key number to burn (default: 1)")
    parser.add_argument("--port", type=str, default=None, help="Serial port to use (default: auto-detect)")
    parser.add_argument("--loop", action="store_true", help="Burn in a loop until Ctrl+C is pressed")
    parser.add_argument("--port-filter", type=str, action="append", default=[], help="Filter for serial ports (e.g., 'USB' to only show USB ports)")
    
    mode_group = parser.add_mutually_exclusive_group()
    mode_group.add_argument("--local", action="store_true", help="Generate combined secret locally (requires MASTER_SECRET env var)")
    mode_group.add_argument("--remote", type=str, help="Generate combined secret remotely via server ")

    parsed_args = parser.parse_args(args)

    secret_generator = None

    if parsed_args.remote:
        from .secret_generator.remote import RemoteSecretGenerator
        api_key = os.environ.get("API_KEY")
        if not api_key:
            raise ValueError("API_KEY environment variable is not set")
        secret_generator = RemoteSecretGenerator(parsed_args.remote, api_key)
    elif parsed_args.local:
        from .secret_generator.local import LocalSecretGenerator
        master_secret = os.environ.get("MASTER_SECRET")
        if not master_secret:
            raise ValueError("MASTER_SECRET environment variable is not set")
        check_master_secret(master_secret)
        secret_generator = LocalSecretGenerator(master_secret)
    else:
        raise ValueError("Either --local or --remote must be specified")

    max_loops = 1 if not parsed_args.loop else float('inf')
    loop_iters = 0
    success_iters = 0

    previous_ports = set()
    success_ports = set()

    while success_iters < max_loops:
        loop_iters += 1
        ports = esptool.get_port_list()
        ports = set(ports)

        added_ports = ports - previous_ports
        removed_ports = previous_ports - ports
        success_ports = success_ports - removed_ports # Re-allow burning on ports that were removed and re-added
        sep = "\n - "
        if added_ports:
            print(f"New device(s) detected: {''.join([sep+p for p in added_ports])}")
        if removed_ports:
            print(f"Device(s) removed: {''.join([sep+p for p in removed_ports])}")
        previous_ports = ports
        ports = ports - success_ports # Filter out ports that have already been successfully burned

        if parsed_args.port_filter:
            ports = [p for p in ports if port_matches(p, set(parsed_args.port_filter))]

        if not ports:
            time.sleep(1)
            print(f"Waiting for device {parsed_args.port or 'auto-detect'}... {LOADING_CHARS[loop_iters % len(LOADING_CHARS)]}", end="\r")
            continue
        port = parsed_args.port or list(ports)[0]
        print(f"Connecting to device on port {port}.")
        try:
            esp = ESP(port=port)
        except:
            print(f"Failed to connect to device on port {port}. Retrying...")
            time.sleep(1)
            continue
        try:
            secret = secret_generator.generate_combined_secret(esp.read_mac())
            esp.burn_hmac_key(secret, key_to_use=parsed_args.key, do_not_confirm=parsed_args.loop)
            success_iters += 1
            success_ports.add(port)
            print()
            print()
            print("Successfully burned HMAC key on device.")
            print(f"{success_iters} of {max_loops if max_loops != float('inf') else '∞'} successful burn(s).")
            print()
            print()
        except Exception as e:
            print()
            print()
            print(f"Failed to burn HMAC key on device. Retrying...")
            print(f"Error: {e}")
            print()
            print()
            time.sleep(1)
            continue
