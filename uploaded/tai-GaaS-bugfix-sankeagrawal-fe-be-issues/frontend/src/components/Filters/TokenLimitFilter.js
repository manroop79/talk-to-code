import React, {useContext} from "react";
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { Accordion, AccordionDetails, AccordionSummary, Switch, Grid, InputLabel, MenuItem, Select, Tooltip, TextField } from "@mui/material";
import { Context } from "../../Store";

export default function TokenLimitFilter(props) {
    const {filterName, helperText} = props;
    const [state, dispatch] = useContext(Context);

    const handleCheck = (event) => {
        dispatch({type: "TOKEN_LIMIT", enabled: event.target.checked})
    };

    const handleTokenTypeChange = (event) => {
        dispatch({type: "TOKEN_LIMIT", encoding_name: event.target.value})
    };
    
    const handleTokenValueChange = (event) => {
        dispatch({type: "TOKEN_LIMIT", limit: event.target.value})
    };

    return (
        <div>
            <Grid sx={{ pt: 2, pb: 2 }} container direction="row" justifyContent="space-evenly" alignItems="center">
                <Switch checked={state.TokenLimit.enabled} onChange={handleCheck}/>
                <Accordion sx={{width: "50%"}}>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>{filterName}</AccordionSummary>
                    <AccordionDetails>
                        <InputLabel>Encoding Name</InputLabel>
                        <Select value={state.TokenLimit.encoding_name} onChange={handleTokenTypeChange}>
                            <MenuItem value="cl100k_base">cl100k_base</MenuItem>
                            <MenuItem value="p50k_base">p50k_base</MenuItem>
                            <MenuItem value="r50k_base">r50k_base</MenuItem>
                        </Select>
                    <TextField sx={{ mt: 3 }} fullWidth value={state.TokenLimit.limit} onChange={handleTokenValueChange} type="number" label="Limit" inputProps={{min: 0, step: 10}}/>
                    </AccordionDetails>
                </Accordion>
                <Tooltip title={helperText} placement="right">
                    <HelpOutlineIcon/>
                </Tooltip>
            </Grid>
        </div>
    );
}