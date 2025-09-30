import React, {useContext} from "react";
import HelpOutlineIcon from '@mui/icons-material/HelpOutline';
import ExpandMoreIcon from '@mui/icons-material/ExpandMore';
import { Accordion, AccordionDetails, AccordionSummary, Autocomplete, Switch, Grid, TextField, Tooltip } from "@mui/material";
import { Context } from "../../Store";

export default function LanguageFilter(props) {
    const {CurrentPage, filterName, helperText} = props;
    const [state, dispatch] = useContext(Context);
    const LANGUAGES = [
        { label: "Arabic", key: "ar" },
        { label: "Bulgarian", key: "bg" },
        { label: "German", key: "de" },
        { label: "Modern Greek", key: "el" },
        { label: "English", key: "en" },
        { label: "Spanish", key: "es" },
        { label: "French", key: "fr" },
        { label: "Hindi", key: "hi" },
        { label: "Italian", key: "it" },
        { label: "Japanese", key: "ja" },
        { label: "Dutch", key: "nl" },
        { label: "Polish", key: "pl" },
        { label: "Portuguese", key: "pt" },
        { label: "Russian", key: "ru" },
        { label: "Swahili", key: "sw" },
        { label: "Thai", key: "th" },
        { label: "Urdu", key: "ur" },
        { label: "Vietnamese", key: "vi" },
        { label: "Chinese", key: "zh" },
    ];
    // const LANGUAGES2 = ["ar","bg","de","el","en","es","fr","hi","it","ja","nl","pl","pt","ru","sw","th","ur","vi","zh"];

    return (
        <div>
            <Grid sx={{ pt: 2, pb: 2 }} container direction="row" justifyContent="space-evenly" alignItems="center">
                <Switch checked={CurrentPage === "input" ? state.Language.enabled : state.Language_OUTPUT.enabled} onChange={(event) => dispatch({type: CurrentPage === "input" ? "LANGUAGE" : "LANGUAGE_OUTPUT", enabled: event.target.checked})}/>
                <Accordion sx={{width: "50%"}}>
                    <AccordionSummary expandIcon={<ExpandMoreIcon />}>{filterName}</AccordionSummary>
                    <AccordionDetails>
                        <Autocomplete
                            clearIcon={false}
                            options={LANGUAGES.map((option) => option.key)}
                            value={CurrentPage === "input" ? state.Language.valid_languages : state.Language_OUTPUT.valid_languages}
                            multiple
                            onChange={(e, value, situation, option) => dispatch({type: CurrentPage === "input" ? "LANGUAGE" : "LANGUAGE_OUTPUT", valid_languages: typeof value === 'string' ? value.split(",") : value})}
                            renderInput={(params) => ( <TextField {...params} label="Allow the following languages..." /> )}
                        />
                    </AccordionDetails>
                </Accordion>
                <Tooltip title={helperText} placement="right">
                    <HelpOutlineIcon/>
                </Tooltip>
            </Grid>
        </div>
    );
}