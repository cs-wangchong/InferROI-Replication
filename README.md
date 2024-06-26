# Replication Package of *InferROI*
This replication package include all the evaluation data and results in our work, and source code will be released upon the accpetance.


## Source Code
Source files can be found in the folders named `app`.
- `llm4leak.py`: Define the main `LLM4Leak` class 
- `cfg.py`: Define the `CFG` class


## Results
- **RQ1:** The detection results for the DroidLeaks and JLeaks datasets can be found in [`results/rq1/droidleaks.log`](./results/rq1/droidleaks.log) and [`results/rq1/jleaks.log`](./results/rq1/jleaks.log).  The detailed execution information of key steps is also included in the log files.

- **RQ2:** The detection results for the 100 open-source methods can be found in [`results/rq2/open-source.log`](./results/rq2/open-source.log). The detailed execution information of key steps is also included in the log file. We submitted 12 pull requests, and 7 of them are confirmed by developers. The pull requests can be found in [`results/rq2/PR.md`](./results/rq2/PR.md)

- **RQ3.a:** The results of the intention inference can be found in [`results/rq3a/intentions.csv`](./results/rq3a/intentions.csv).


- **RQ3.b:** The results of GPTLeak and GPTLeak-chain can be found in [`results/rq3b/gptleak.csv`](./results/rq3b/gptleak.csv) and [`results/rq3b/gptleak-chain.csv`](./results/rq3b/gptleak.csv).



## Reproduction

### Environment
- python >= 3.9
- dependencies: `openai`, `langchain`, `spacy`, `srctoolkit`

### Data
Download datasets using this figshare [link](https://figshare.com/s/6b5623b4d2a18cf1e66e). Unzip the `data.zip` file, which includes the DroidLeaks and JLeaks dataset and the 100 open-source methods

### Evaluation Scripts
The scripts used to evaluate InferROI are included in the `script` folder.
- `script/scan_droidleaks.py`: Detect resource leaks for the DroidLeaks dataset
- `script/scan_jleaks.py`: Detect resource leaks for the JLeaks dataset
- `script/scan_open_source.py`: Detect resource leaks for the 100 open source methods
