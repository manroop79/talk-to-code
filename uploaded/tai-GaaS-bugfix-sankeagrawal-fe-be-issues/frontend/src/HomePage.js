import React, {useState} from "react";
import {Box, Grid, Tab, Tabs, Typography} from "@mui/material";
import PromptComponent from "./components/PromptComponent";
import InputScanners from "./components/InputScanners";
import OutputScanners from "./components/OutputScanners";

export default function HomePage(props) {
    const [value, setValue] = useState(0);

    const handleChange = (event, newValue) => {
        setValue(newValue);
    };

    return (
        <div>
            <Grid container direction="row" justifyContent="center" padding={10}>
                <Grid item width="50%">
                    <Grid container direction="column">
                        <Grid item marginBottom={5}>
                            <Typography variant="h3" display="inline">Trustworthy</Typography>
                            <Typography variant="h3" display="inline" color="#87BC1F">LLM</Typography>
                            <Typography paddingTop={1} paddingBottom={1}>This page demonstrates how the TrustworthyAI framework can be applied to a chat service with an LLM.</Typography>
                        </Grid>
                        <Grid item>
                            {/* This is the box that contains the 3 tabs/toggles */}
                            <Box marginBottom={5} sx={{ borderBottom: 1, borderColor: 'divider' }}>
                                <Tabs value={value} onChange={handleChange} centered>
                                    <Tab label="Prompt" />
                                    <Tab label="Input Scanners" />
                                    <Tab label="Output Scanners" />
                                </Tabs>
                            </Box>
                        </Grid>
                        <Grid item>
                            {value === 0 ? <PromptComponent/> : null}
                            {value === 1 ? <InputScanners CurrentPage="input"/> : null}
                            {value === 2 ? <OutputScanners CurrentPage="output"/> : null}
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
        </div>
    )
}