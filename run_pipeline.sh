#!/usr/bin/env bash
sbatch \
  --mail-type=END \
  --mem-per-cpu=2000 \
  --time=120:00:00 \
  -o snake.out -e snake.err \
snakemake \
  --profile profile_simple/ \
  -s workflow/Snakefile \
  --rerun-incomplete \
  --keep-incomplete \
  -pr \
  --cores 200 \
  --use-conda \
  --latency-wait 30 \
  --show-failed-logs \
  "$@"
