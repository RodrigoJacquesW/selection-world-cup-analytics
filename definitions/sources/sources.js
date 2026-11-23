// Raw tables loaded by main.py (dataset from the `raw_dataset` var).
const rawDataset = dataform.projectConfig.vars.raw_dataset;

[
  { name: "matches", description: "SofaScore matches of the tracked teams (snapshot)." },
  { name: "match_stats", description: "SofaScore match statistics, one column per stat and side, as text." },
  { name: "elo_ratings", description: "World Football Elo Ratings (eloratings.net World.tsv)." },
  { name: "teams", description: "Reference: the 29 tracked national teams." },
  { name: "elo_codes", description: "Reference: SofaScore team name -> eloratings.net code." },
].forEach(({ name, description }) => declare({ schema: rawDataset, name, description }));
