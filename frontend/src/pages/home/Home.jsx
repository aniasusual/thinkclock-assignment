import { Grid, Button, Typography } from '@material-ui/core';
import { Link } from "react-router-dom";
import "./home.scss"

function Home() {

    return (
        <div id='homePage'>
            <div id="homeHeading">
                <Typography style={{ margin: 50, color: "white" }} variant="h2">
                    Cell Information
                </Typography>
            </div>
            <div id="homeContent">
                <Grid container spacing={6}>
                    <Grid item xs={6}>
                        <Link to="/barcode_generator">
                            <Button variant="contained" size="small" color="secondary">
                                <svg xmlns="http://www.w3.org/2000/svg" width="300" height="300" style={{ padding: 30 }} fill="currentColor" class="bi bi-upc" viewBox="0 0 16 16">
                                    <path d="M3 4.5a.5.5 0 0 1 1 0v7a.5.5 0 0 1-1 0v-7zm2 0a.5.5 0 0 1 1 0v7a.5.5 0 0 1-1 0v-7zm2 0a.5.5 0 0 1 1 0v7a.5.5 0 0 1-1 0v-7zm2 0a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-7zm3 0a.5.5 0 0 1 1 0v7a.5.5 0 0 1-1 0v-7z" />
                                </svg>
                            </Button>
                        </Link>
                    </Grid>
                    <Grid item xs={6}>
                        <Link to="/barcode_scanner">
                            <Button variant="contained" size="large" color="secondary">
                                <svg xmlns="http://www.w3.org/2000/svg" width="300" height="300" style={{ padding: 30 }} fill="currentColor" class="bi bi-upc-scan" viewBox="0 0 16 16">
                                    <path d="M1.5 1a.5.5 0 0 0-.5.5v3a.5.5 0 0 1-1 0v-3A1.5 1.5 0 0 1 1.5 0h3a.5.5 0 0 1 0 1h-3zM11 .5a.5.5 0 0 1 .5-.5h3A1.5 1.5 0 0 1 16 1.5v3a.5.5 0 0 1-1 0v-3a.5.5 0 0 0-.5-.5h-3a.5.5 0 0 1-.5-.5zM.5 11a.5.5 0 0 1 .5.5v3a.5.5 0 0 0 .5.5h3a.5.5 0 0 1 0 1h-3A1.5 1.5 0 0 1 0 14.5v-3a.5.5 0 0 1 .5-.5zm15 0a.5.5 0 0 1 .5.5v3a1.5 1.5 0 0 1-1.5 1.5h-3a.5.5 0 0 1 0-1h3a.5.5 0 0 0 .5-.5v-3a.5.5 0 0 1 .5-.5zM3 4.5a.5.5 0 0 1 1 0v7a.5.5 0 0 1-1 0v-7zm2 0a.5.5 0 0 1 1 0v7a.5.5 0 0 1-1 0v-7zm2 0a.5.5 0 0 1 1 0v7a.5.5 0 0 1-1 0v-7zm2 0a.5.5 0 0 1 .5-.5h1a.5.5 0 0 1 .5.5v7a.5.5 0 0 1-.5.5h-1a.5.5 0 0 1-.5-.5v-7zm3 0a.5.5 0 0 1 1 0v7a.5.5 0 0 1-1 0v-7z" />
                                </svg>
                            </Button>
                        </Link>
                    </Grid>
                </Grid>
            </div>

        </div>
    );
}

export default Home;
