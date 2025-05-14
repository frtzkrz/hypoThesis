# `hypoThesis`

This file is mostly copied from the README of the [`lynference`] repository created by Roman Ludwig.
This repository serves the purpose of recreating the results in my Bachelors thesis "Modeling Lymphatic Progression of Hypopharyngeal Squamous Cell Carcinomas".
For the metrics of the different graphs, DVC is used because the data files are mostly too large to handle otherwise. For the plots of prevalences and risk assassements, git is used.

> :warning: **NOTE:** \
> We highly recommend using a virtual environment for anything that comes below. Feel free to use any tool you are comfortable with. We use [venv], and you can use these commands to get your virtual environment started:
> ```bash
> python3 -m venv .venv
> source .venv/bin/activate
> pip install --upgrade pip setuptools wheel
> ```

All requirements can be installed using [pip] and the `requirements.txt` file at the root of this repository:

```bash
pip install -r requirements.txt
```

This will install these three packages and its dependencies:
* [DVC], which is a tool that allows the versioning of arbitrary data and pipelines, while keeping git uncluttered.
* [`lymph-model`]: The implementation of our mathematical model on lymphatic spread [[1]](#1)
* [`lyscripts`]: A command line interface (CLI) to perform the various steps of the pipeline. 


[![up-button]](#lynference)


## :recycle: Reproduce a Pipeline

[DVC] makes pipelines persistent using *pipeline files* (like the `dvc.yaml` at the root and the one inside the `pipeline` directory) that detail how [DVC] should execute various commands and how they depend on each other. After a successful run of a pipeline, [DVC] stores the MD5 hashes of all produced files in the `dvc.lock` file. This allows us to store the data - which may be binary and/or very large - to be stored elsewhere, while [DVC] will still know how to find it.

To reproduce a pipeline, follow these steps:

### 1. Clone Repository

Clone this repository, enter it and checkout the revision of the pipeline you're interested in. Usually, this would be the name of a tag:

```bash
git clone https://github.com/frtzkrz/hypoThesis
cd hypoThesis
```


### 2. Start the pipeline

Finally, the pipeline can be launched. If everything works as intended the command below should launch the pipeline. Note that it may take quite some time to finish (something on the order of hours). But during the entire process, it should keep you updated about what's happening.

```bash
git checkout <tag-of-interest>
dvc repro pipeline/dvc.yaml
```

| Graph tags |
|-------|
| ex_A |
| ex_B |
| ex_C |
| base_A |
| base_B |
| base_C |
| base_D |
| base_A |
| V_A |
| V_B |
| V_C |
| V_D |
| V_E |
| V_F |
| I_A |
| I_B |
| I_C |
| VI_VII_A |
| VI_VII_B |
| VI_VII_C |
| VI_VII_D |

### 3. Recreate Prevalence Plots

```bash
git checkout <revision-of-interest>
python3 thesis_plots/scripts/prevalences.py
```

| Prevalence Plot  | tag      |
|---------------|--------  |
| Example (a)           | prev_ex1  |
| Example (b)           | prev_ex2  |
| Base (a)           | prev_base1 |
| Base (b)           | prev_base2 |
| V           | prev_V |
| I (a)           | prev_I1 |
| I (b)           | prev_I2 |
| VI & VII (a)           | prev_VI_VII1 |
| VI & VII (b)           | prev_VI_VII2 |

The plots will be saved to thesis_plots/plots/prevalences.

### 4. Recreate Risk Plots

```bash
git checkout <revision-of-interest>
python3 thesis_plots/scripts/risks.py
```

| Risk to LNL   | tag      |
|---------------|--------  |
| III           | riskIII  |
| IV            | riskIV   |
|  V            | risk V   |

The plots will be saved to thesis_plots/plots/risks.




### 5. Cleaning up

Assuming you have used [venv], all you need to do to erase the entire virtual environment, the repository, pipeline and all associated data is to deactivate the environment, leave the repository and delete it

```bash
deactivate
cd ..
rm -rf hypoThesis
```


[![up-button]](#lynference)

[`lynference`]: https://github.com/rmnldwg/lynference
[venv]: https://python.readthedocs.io/en/stable/library/venv.html
[pip]: https://pip.pypa.io/en/stable/
[conda]: https://docs.conda.io/en/latest/
[DVC]: https://dvc.org
[`lyDATA`]: https://github.com/rmnldwg/lydata
[`lyscripts`]: https://github.com/rmnldwg/lyscripts
[`lymph-model`]: https://github.com/rmnldwg/lymph
[`lymph`]: https://github.com/rmnldwg/lymph
[`dvc get`]: https://dvc.org/doc/command-reference/get
[`bilateral-v1`]: https://github.com/rmnldwg/lynference/releases/tags/bilateral-v1
[`midline-with-mixing-v1`]: https://github.com/rmnldwg/lynference/releases/tags/midline-with-mixing-v1
[`midline-without-mixing-v1`]: https://github.com/rmnldwg/lynference/releases/tags/midline-without-mixing-v1
[zenodo]: https://zenodo.org
[releases]: https://github.com/rmnldwg/lynference/releases

[up-button]: https://dabuttonfactory.com/button.png?t=back+to+top&f=Roboto-Bold&ts=15&tc=eef&hp=16&vp=5&c=6&bgt=unicolored&bgc=89a
