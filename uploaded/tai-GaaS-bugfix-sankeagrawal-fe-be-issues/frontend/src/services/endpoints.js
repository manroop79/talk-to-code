const CleanScanInput = (NewRequestData) => {
    // This function takes the React context and cleans it for the backend input scanner.
    const scanner_configs = {};
    Object.keys(NewRequestData).forEach(key => {
        if (key !== "prompt" && key !== "fail_fast" && key !== "prompt_helpers") {
            if (!key.endsWith("_OUTPUT")) {
                // These are input scanners
                scanner_configs[key] = NewRequestData[key];
                delete NewRequestData[key];
            }
            if (key.endsWith("_OUTPUT")) {
                // These are output scanners. Don't care for this function.
                delete NewRequestData[key];
            }
        }
    });
    NewRequestData["scanner_configs"] = scanner_configs;
    return NewRequestData;
};

const CleanScanOutput = (NewRequestData) => {
    // This function takes the React context and cleans it for the backend output scanner.
    const scanner_configs = {};
    Object.keys(NewRequestData).forEach(key => {
        if (key !== "prompt" && key !== "fail_fast" && key !== "prompt_helpers") {
            if (!key.endsWith("_OUTPUT")) {
                // These are input scanners. Don't care for this function.
                delete NewRequestData[key];
            }
            if (key.endsWith("_OUTPUT")) {
                // These are output scanners. Remove trailing "_OUTPUT" when creating object key
                scanner_configs[key.slice(0,-7)] = NewRequestData[key];
                delete NewRequestData[key];
            }
        }
    });
    NewRequestData["scanner_configs"] = scanner_configs;
    return NewRequestData;
};

class EndpointService {
    async ScanInputWait(requestData) {
        // Copy data to new object
        let NewRequestData = {...requestData};
    
        // Clean up the request object for API
        const CleanData = CleanScanInput(NewRequestData);
        console.log(CleanData);
    
        const response = await fetch("http://a402c798ba0bf424586c958a8730ac8c-420265549.us-east-1.elb.amazonaws.com/run_input_scanners", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(CleanData)
        });
        const json = await response.json();
        return json;
    }

    async GenerateTextWait(sanitized_prompt) {
        const response = await fetch("http://af8c0b283d3bb441fab1f907792d4bc4-2016684669.us-east-1.elb.amazonaws.com/generate", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify({"inputs": sanitized_prompt, "parameters":{"max_new_tokens":200}})
        });
        const json = await response.json();
        return json;
    }

    async ScanOutputWait(requestData) {
        // Copy data to new object
        let NewRequestData = {...requestData};

        // Clean up the request object for API
        const CleanData = CleanScanOutput(NewRequestData);
        console.log(CleanData);

        return fetch("http://a402c798ba0bf424586c958a8730ac8c-420265549.us-east-1.elb.amazonaws.com/run_output_scanners", {
            method: "POST",
            headers: {"Content-Type": "application/json"},
            body: JSON.stringify(CleanData)
        }).then((response) => {
            if (!response.ok) {
                console.log(`HTTP Error. Status = ${response.status}`);
            }
            return response.json();
        }).then((data) => {
            return data;
        }).catch((error) => {
            console.log(error);
        })
    }
}

export default EndpointService;
