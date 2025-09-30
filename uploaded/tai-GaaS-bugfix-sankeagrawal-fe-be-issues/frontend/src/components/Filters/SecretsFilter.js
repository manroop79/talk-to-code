import React, {useContext} from "react";
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { Accordion, AccordionDetails, AccordionSummary, Switch, Grid, InputLabel, MenuItem, Select, Tooltip } from "@mui/material";
import { Context } from "../../Store";

export default function SecretsFilter(props) {
    const {filterName, helperText} = props;
    const [state, dispatch] = useContext(Context);

    const handleCheck = (event) => {
        dispatch({type: "SECRETS", enabled: event.target.checked})
    };

    const handleChange = (event) => {
        dispatch({type: "SECRETS", redact_mode: event.target.value})
    };

    return (
        <div>
            <Grid sx={{ pt: 2, pb: 2 }} container direction="row" justifyContent="space-evenly" alignItems="center">
                <Switch checked={state.Secrets.enabled} onChange={handleCheck}/>
                <Accordion sx={{width: "50%"}}>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>{filterName}</AccordionSummary>
                    <AccordionDetails>
                        <InputLabel>Redact Mode</InputLabel>
                        <Select value={state.Secrets.redact_mode} onChange={handleChange}>
                            <MenuItem value="all">all</MenuItem>
                            <MenuItem value="partial">partial</MenuItem>
                            <MenuItem value="hash">hash</MenuItem>
                        </Select>
                    </AccordionDetails>
                </Accordion>
                <Tooltip title={helperText} placement="right">
                    <HelpOutlineIcon/>
                </Tooltip>
            </Grid>
        </div>
    );
}