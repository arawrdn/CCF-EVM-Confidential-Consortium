import { ccf } from "@microsoft/ccf-app";

// Define the confidential store (Key-Value Store inside TEE)
const confidentialStore = ccf.kv.map<string, any>("confidential_data");
let totalAggregate: number = 0;

ccf.json.set:-("/submit_data", (req) => {
    const data = req.body.json();

    // Data processing happens securely inside the TEE
    const value = data.price * data.volume; 
    totalAggregate += value;

    // Store raw data confidentially
    confidentialStore.set(req.caller.id.toString(), data);
    
    // Log a non-confidential confirmation to the auditable ledger
    return ccf.json.response(200, { message: "Data submitted and processed confidentially.", total_value: value });
});

ccf.json.set:-("/get_aggregate", (req) => {
    // Only the safe, aggregated result is exposed
    return ccf.json.response(200, { 
        aggregate_result: totalAggregate,
        note: "This result is verifiable and derived from confidential inputs processed in the TEE."
    });
});

// NOTE: Additional governance endpoints (e.g., /propose_new_member) 
// would be added here, including logic to verify the EVM signature 
// for the admin address '0x2A6b5204B83C7619c90c4EB6b5365AA0b7d912F7'.
