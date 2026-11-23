// Elo-weighted average that ignores matches where the metric is missing.
// SUM(x * w) / SUM(w) would keep the weight of a NULL x in the denominator and
// pull the team's average towards zero.
function weighted_avg(column, weight = "weight") {
  return `safe_divide(sum(${column} * ${weight}), sum(if(${column} is null, null, ${weight})))`;
}

// Z-score across all teams. Use higher_is_better = false for "conceded" metrics.
function zscore(column, higher_is_better = true) {
  const diff = higher_is_better
    ? `${column} - avg(${column}) over ()`
    : `avg(${column}) over () - ${column}`;
  return `safe_divide(${diff}, stddev_pop(${column}) over ())`;
}

// Pillar weights of the final score (must add up to 1).
const PILLAR_WEIGHTS = { attack: 0.30, defense: 0.25, control: 0.20, differential: 0.15, efficiency: 0.10 };

module.exports = { weighted_avg, zscore, PILLAR_WEIGHTS };
