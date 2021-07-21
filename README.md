# GitHub Action: Parse flags

## Description

Action to parse flags from `pull request` or `push`.

Flags are texts enclosed in square brackets

```
[bump ver minor]
[skip ci]
[backend]
```

spaces and text case does not matter in flags

```
[   BuMp  Ver    MInor  ] is converted to [bump ver minor]
```

flags are returned as a list of lowercased texts in square brackets (JSON format).

```
["[bump ver minor]", "[skip ci]", "[backend]"]
```

How GitHub event content is parsed for flags:

```
pull request labels         - converted into flags

pull request title          - parsed for flags

push head_commit message    - parsed for flags
```

## Requirements

Action requires `python` to be installed on `runner`.

Hint: [github.com/actions/setup-python](https://github.com/actions/setup-python)

## Inputs

```
none
```

## Outputs

```
flags            - parsed flags as JSON or null (when no flags detected)
                   i.e. '{"labels": ["[bump ver minor]", "[backend]"], "text": ["[skip ci]"]}'
```

## Usage

### Sample workflow definition `pull request`

```
name: Sample workflow

on:
  pull_request:
    branches:
      - main
    types: [closed]

jobs:
  sample:
    runs-on: ubuntu-latest
    steps:
      - name: Execute action parse flags
        id: flags
        uses: all4group/github-action-parse-flags@v2
      - name: Step with flags
        if: ${{ fromJSON(steps.flags.outputs.flags) }}
        run: |
          if [ "${{ contains(fromJSON(steps.flags.outputs.flags).labels, '[skip ci]') }}" == "true" ]; then
            echo "=> [skip ci] flag detected in pull request labels"
          elif [ "${{ contains(fromJSON(steps.flags.outputs.flags).text, '[skip ci]') }}" == "true" ]; then
            echo "=> [skip ci] flag detected in pull request title"
          else
            echo "=> [skip ci] flag not detected"
          fi
        shell: bash
      - name: Step without flags
        if: ${{ !fromJSON(steps.flags.outputs.flags) }}
        run: echo "=> no flags detected"
        shell: bash
```

### Sample workflow definition `push`

```
name: Sample workflow

on:
  push:
    branches:
      - main

jobs:
  sample:
    runs-on: ubuntu-latest
    steps:
      - name: Execute action parse flags
        id: flags
        uses: all4group/github-action-parse-flags@v2
      - name: Step with flags
        if: ${{ fromJSON(steps.flags.outputs.flags) }}
        run: |
          if [ "${{ contains(fromJSON(steps.flags.outputs.flags).text, '[skip ci]') }}" == "true" ]; then
            echo "=> [skip ci] flag detected in push head_commit message"
          else
            echo "=> [skip ci] flag not detected"
          fi
        shell: bash
      - name: Step without flags
        if: ${{ !fromJSON(steps.flags.outputs.flags) }}
        run: echo "=> no flags detected"
        shell: bash
```
