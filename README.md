[![Pytest](https://github.com/languagetooler-gmbh/rule-creation-stats/actions/workflows/pytest.yml/badge.svg)](https://github.com/languagetooler-gmbh/rule-creation-stats/actions/workflows/pytest.yml)
[![Flake8](https://github.com/p-goulart/rule-id-dump/actions/workflows/flake8.yml/badge.svg)](https://github.com/p-goulart/rule-id-dump/actions/workflows/flake8.yml)

# Rule Creation Stats
This project contains a bunch of scripts used to dump rule IDs, count them, diff them, etc.

## Schedule
All of the scripts listed here are set to run at 3AM every weekday.

## Quarterly stats
The start of the quarter is defined arbitrarily by tagging our repos with a tag such as `2023q1`. This tag is arbitrary and, therefore, must be updated manually in the GitHub Actions variables of this repo (@p-goulart can do this).

## Scripts
### Summary

|script|artefact name|artefact contents|
|---|---|---|
|dump_all|rule-dump-latest|a flat list of all current rule IDs|
|compare|added-rules|a flat list of all rule IDs added **in the current quarter**|
|master_csv|all_rules|a massive CSV containinng data for every single rule in every locale|
|style_stats|style_stats|`all_time_summary.txt`: all currently `tone_tag`ged rules;`added_this_quarter.txt` changes in style rules as a differential in tone tag numbers|

### `dump_all`

This simple utility can serve as a sort of sanity test for the code here. All it does is print out a list of unique rule IDs from the **latest** XML files on the `master` branch of both the OS and premium repositories, e.g.:

```
ABKUERZUNG_FALSCHE_PUNKTE
ABKUERZUNG_FEHLENDE_PUNKTE
ABKUERZUNG_LEERZEICHEN
ABLAUF_SUBST
ABRAHAM_LINCOLN
ABREITEN_VS_ARBEITEN
ABSAGE_SUBST
```

#### Artefact structure

```
├── de
│   ├── os.txt
│   └── premium.txt
├── en
│   ├── os.txt
│   └── premium.txt
├── es
│   ├── os.txt
│   └── premium.txt
├── fr
│   ├── os.txt
│   └── premium.txt
├── nl
│   ├── os.txt
│   └── premium.txt
└── pt
    ├── os.txt
    └── premium.txt
```

### `compare`

A version of `dump_all` that only prints rule IDs created in the **current quarter**, e.g.:

```
ABKUERZUNG_FALSCHE_PUNKTE
ABKUERZUNG_FEHLENDE_PUNKTE
ABKUERZUNG_LEERZEICHEN
ABLAUF_SUBST
ABRAHAM_LINCOLN
ABREITEN_VS_ARBEITEN
ABSAGE_SUBST
```


#### Artefact structure

```
├── de
│   ├── os.txt
│   └── premium.txt
├── en
│   ├── os.txt
│   └── premium.txt
├── es
│   ├── os.txt
│   └── premium.txt
├── fr
│   ├── os.txt
│   └── premium.txt
├── nl
│   ├── os.txt
│   └── premium.txt
└── pt
    ├── os.txt
    └── premium.txt
```

### `master_csv`

This script is meant to provide an all-encompassing view of **all** rules created by the lingu team in **one single file** – this means *all locales* are present in the same file. For example:

```csv
row,id,subId,locale,source_repo,type,source_file,tone_tags,writing_goals,is_goal_specific
0,IN_SHANGHAI,1,en,os,grammar,grammar.xml,,,false
1,IN_SHANGHAI,2,en,os,grammar,grammar.xml,,,false
2,LOWERCASE_NAMES,1,fr,premium,grammar,grammar.xml,,,false
3,SOME_EXAMPLE,1,es,os,style,grammar.xml,professional,serious,true
```

#### Table headers

|header|description|
|---|---|
|row|row number, not unique or stable, please don't use this for anything programmatic|
|id|rule ID – if the rule is a sub-rule of a rulegroup, the ID will be that of the rulegroup|
|subId| sub rule ID – index of a (sub-)rule. The subId of a standalone rule is always `[1]`|
|source_repo|'os' or 'premium'|
|type|'grammar', 'style', or 'unknown'|
|source_file|the path to the file where this rule comes from|
|tone_tags|comma-separated list of `tone_tags` applied to the the rule, including those inherited from rulegroups and categories|
|writing_goals|comma-separate list of writing goals served by the tone tags in the previous column|
|is_goal_specific|boolean value of `is_goal_specific` rule attribute|


### `style_stats`

This script generates **two** types of artefacts.

The `all_time_summary.txt` files contain a count of the **latest** (per `master` branch) rule counts **per `tone_tag`** (or `writing_goal`).

For each report we also have a few special categories:

* `tagged` refers to all tagged rules;
* `untagged` refers to... you guessed it... all **untagged** rules 🥴
* `unique_rules` refers to the actual number of rules – since rules may contain multiple different tags, the sum in `total` could be misleading.

Here's an example for **tone tags** counted for a single language:

```
   repo    tone_tags  count
     os     academic      1
     os      clarity    137
     os    confident      7
     os       formal     73
     os      general      3
     os     informal    923
     os       tagged   1144
     os        total   1144
     os unique_rules   1006
     os     untagged    416
premium     academic     12
premium      clarity     85
premium    confident      3
premium       formal     76
premium      general      6
premium   persuasive      5
premium professional     27
premium       tagged    214
premium        total    214
premium unique_rules    175
```

The `added_this_quarter.txt` files provide us with the differential for **the current quarter**. Each positive value means we can count more rules for that tone tag/writing goal now than at the beginning of the quarter, and a negative value means that we can count fewer (i.e. rules have been deleted or re-tagged).

For example, the following data (per writing goal) tells us that we have 'lost' 11 `personal` rules and 'gained' 60 `objective` ones:

```
tagged,94
serious,87
objective,60
confident,0
personal,-5
expressive,-6
untagged,0
```

#### Artefact structure

We generate each artefact for each **locale** (as well as a combined total of all locales) and for either writing goal or tone tag.

```
.
├── all
│   ├── tone_tags
│   │   └── all_time_summary.txt
│   └── writing_goals
│       └── all_time_summary.txt
├── de
│   ├── added_this_quarter.txt
│   ├── all_time_summary.txt
│   ├── tone_tags
│   │   ├── added_this_quarter.txt
│   │   └── all_time_summary.txt
│   └── writing_goals
│       ├── added_this_quarter.txt
│       └── all_time_summary.txt
├── en
│   ├── added_this_quarter.txt
│   ├── all_time_summary.txt
│   ├── tone_tags
│   │   ├── added_this_quarter.txt
│   │   └── all_time_summary.txt
│   └── writing_goals
│       ├── added_this_quarter.txt
│       └── all_time_summary.txt
├── es
│   ├── added_this_quarter.txt
│   ├── all_time_summary.txt
│   ├── tone_tags
│   │   ├── added_this_quarter.txt
│   │   └── all_time_summary.txt
│   └── writing_goals
│       ├── added_this_quarter.txt
│       └── all_time_summary.txt
├── fr
│   ├── added_this_quarter.txt
│   ├── all_time_summary.txt
│   ├── tone_tags
│   │   ├── added_this_quarter.txt
│   │   └── all_time_summary.txt
│   └── writing_goals
│       ├── added_this_quarter.txt
│       └── all_time_summary.txt
├── nl
│   ├── added_this_quarter.txt
│   ├── all_time_summary.txt
│   ├── tone_tags
│   │   ├── added_this_quarter.txt
│   │   └── all_time_summary.txt
│   └── writing_goals
│       ├── added_this_quarter.txt
│       └── all_time_summary.txt
└── pt
    ├── added_this_quarter.txt
    ├── all_time_summary.txt
    ├── tone_tags
    │   ├── added_this_quarter.txt
    │   └── all_time_summary.txt
    └── writing_goals
        ├── added_this_quarter.txt
        └── all_time_summary.txt
```
