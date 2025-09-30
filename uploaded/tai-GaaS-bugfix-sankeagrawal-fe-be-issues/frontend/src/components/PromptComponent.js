import React, {useContext, useState} from "react";
import { Alert, AlertTitle , Backdrop, Button, CircularProgress, Stack, TextField } from "@mui/material";
import { Context } from "../Store";

import EndpointService from "../services/endpoints";
const endpointService = new EndpointService();

export default function PromptComponent(props) {
    const [state, dispatch] = useContext(Context);
    const [open, setOpen] = useState(false);
    
    const handleClose = () => {
        setOpen(false);
    };
    
    const handleOpen = () => {
        setOpen(true);
    };

    return (
        <div>
        <Backdrop sx={{ color: '#fff', zIndex: (theme) => theme.zIndex.drawer + 1 }} open={open}>
            <CircularProgress color="inherit" />
        </Backdrop>
        <Stack spacing={3}>
            <TextField fullWidth label="Enter your prompt..." multiline rows={4} value={state.prompt} onChange={(e) => {dispatch({type: "prompt", value: e.target.value})}}/>
            <Button size="large" variant="outlined" onClick={() => ScanInputWait()}>Scan Prompt</Button>
            {state.prompt_helpers.InvalidPrompt ? <Alert severity="error">Your prompt violated the LLM usage policy</Alert> : null}
            {state.prompt_helpers.SanitizedPrompt ? <Alert severity="info"><AlertTitle>Sanitized prompt...</AlertTitle>{state.prompt_helpers.SanitizedPrompt}</Alert> : null}
            {state.prompt_helpers.GeneratedText !== "" ? <Alert severity="success"><AlertTitle>Open AI Result...</AlertTitle>{state.prompt_helpers.GeneratedText}</Alert> : null}
        </Stack>
        </div>
    );

    function ScanInputWait() {
        // Clear the results
        dispatch({type: "PROMPT_HELPERS", SanitizedPrompt: ""});
        dispatch({type: "PROMPT_HELPERS", GeneratedText: ""});
        dispatch({type: "PROMPT_HELPERS", InvalidPrompt: false});
        handleOpen();
        endpointService.ScanInputWait(state).then((value) => {
            if (value !== null) {
                dispatch({type: "PROMPT_HELPERS", SanitizedPrompt: value?.sanitized_prompt});
                dispatch({type: "PROMPT_HELPERS", is_valid: value?.is_valid});
                if (!value?.is_valid) {
                    dispatch({type: "PROMPT_HELPERS", InvalidPrompt: true});
                    handleClose();
                } else {
                    GenerateTextWait(value?.sanitized_prompt);
                }
            } else {
                GenerateTextWait(state.prompt);
            }
        })
    }

    function GenerateTextWait(PromptToSend) {
        endpointService.GenerateTextWait(PromptToSend).then((value) => {
            console.log(value);
            dispatch({type: "PROMPT_HELPERS", GeneratedText: value?.generated_text});
            handleClose();
        })
    }
}
