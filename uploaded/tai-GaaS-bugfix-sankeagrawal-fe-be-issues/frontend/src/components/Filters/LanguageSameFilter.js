import React, {useContext} from "react";
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import { Accordion, AccordionSummary, Switch, Grid, Tooltip } from "@mui/material";
import { Context } from "../../Store";

export default function LanguageSameFilter(props) {
    const {filterName, helperText} = props;
    const [state, dispatch] = useContext(Context);

    const handleCheck = (event) => {
        dispatch({type: "LanguageSame_OUTPUT", enabled: event.target.checked});
    };

    return (
        <div>
            <Grid sx={{ pt: 2, pb: 2 }} container direction="row" justifyContent="space-evenly" alignItems="center">
                <Switch checked={state.LanguageSame_OUTPUT.enabled} onChange={handleCheck}/>
                <Accordion sx={{width: "50%"}} disabled>
                    <AccordionSummary>{filterName}</AccordionSummary>
                </Accordion>
                <Tooltip title={helperText} placement="right">
                    <HelpOutlineIcon/>
                </Tooltip>
            </Grid>
        </div>
    );
}