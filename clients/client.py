import subprocess
import argparse
import json
import os

# --- Configuration ---
NETWORK_HOST = "[https://127.0.0.1:8000](https://127.0.0.1:8000)"
SERVICE_CERT = "service_cert.pem" 
MEMBER_KEY = "member0_privk.pem"
MEMBER_CERT = "member0_cert.pem"

def run_ccf_query(endpoint, method="POST", data=None):
    """Executes a query against the CCF network using the ccf_client utility."""
    
    cmd = [
        "ccf_client.sh", 
        "--rpc-protocol", "http", 
        "--ccf-url", NETWORK_HOST,
        "--ca", SERVICE_CERT,
        "--cert", MEMBER_CERT,
        "--key", MEMBER_KEY,
        "--method", method,
        "--url", f"/app/{endpoint}"
    ]

    if data is not None:
        cmd.extend(["--body", json.dumps(data)])

    try:
        # Executes the shell command and captures output
        result = subprocess.run(cmd, capture_output=True, text=True, check=True)
        print(f"Response from {endpoint}:\n{result.stdout}")
        return result.stdout
    except subprocess.CalledProcessError as e:
        print(f"Error executing CCF query for {endpoint}: {e.stderr}")
        return None

def submit_governance_action(action, proposal_id=None, approve=None, new_member_cert=None):
    """Placeholder for complex governance transactions."""
    
    # NOTE: In a complete implementation, this function would handle:
    # 1. Reading the proposal details or new member certificate.
    # 2. If the action is critical (e.g., 'propose_new_member'), 
    #    it would generate an EVM signature from the admin's private key 
    #    and include it in the transaction metadata for TEE verification.
    
    data = {"action": action}
    if proposal_id is not None:
        data["proposal_id"] = proposal_id
    if approve is not None:
        data["approve"] = approve
    if new_member_cert:
        data["new_member_cert"] = new_member_cert
        
    print(f"Submitting governance action: {action}")
    run_ccf_query("gov/submit_proposal", method="POST", data=data) # Using a generic governance endpoint


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="CCF Client CLI for Confidential Consortium.")
    parser.add_argument("--action", required=True, 
                        choices=["activate", "submit_data", "get_aggregate", "propose_add_member", "vote"], 
                        help="Action to perform.")
    parser.add_argument("--data", type=str, help="JSON data payload for submission.")
    parser.add_argument("--proposal_id", type=int, help="ID of the governance proposal.")
    parser.add_argument("--approve", type=bool, help="Vote (True/False) on a proposal.")
    parser.add_argument("--new_member_cert", type=str, help="Path to the new member's public certificate.")
    
    args = parser.parse_args()

    if args.action == "activate":
        run_ccf_query("gov/activate", method="POST", data={}) 
    elif args.action == "propose_add_member":
        if not args.new_member_cert:
            print("Error: --new_member_cert is required for propose_add_member.")
        else:
            submit_governance_action(args.action, new_member_cert=args.new_member_cert)
    elif args.action == "vote":
        if args.proposal_id is None or args.approve is None:
            print("Error: --proposal_id and --approve are required for vote.")
        else:
            submit_governance_action(args.action, proposal_id=args.proposal_id, approve=args.approve)
    elif args.action == "submit_data":
        if not args.data:
            print("Error: --data is required for submit_data action.")
        else:
            payload = json.loads(args.data)
            run_ccf_query("submit_data", method="POST", data=payload)
    elif args.action == "get_aggregate":
        run_ccf_query("get_aggregate", method="GET")
