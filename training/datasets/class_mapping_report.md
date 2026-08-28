# FreshGuard Vision V3 — Class Mapping & Compatibility Report

## Overview
This report provides a strict, unambiguous mapping between the extracted Roboflow dataset classes and the protected FreshGuard 35-Class V2 production vocabulary.

> [!IMPORTANT]
> **Production Class Isolation**: The 35 production classes (IDs 0–34) are byte-for-byte isolated. Dataset class IDs are NOT blindly assumed to match FreshGuard class IDs.

## Class Mapping Matrix

| Extracted Class ID | Extracted Class Name | FreshGuard V2 ID | FreshGuard Class Name | Compatibility Status | Recommended Mapping |
| :--- | :--- | :--- | :--- | :--- | :--- |
| `0` | `avocado` | `N/A` | `N/A` | **NO MATCH (New Class)** | Candidate for V3 Expansion ('avocado') |
| `1` | `beans` | `N/A` | `N/A` | **NO MATCH (New Class)** | Candidate for V3 Expansion ('beans') |
| `2` | `beet` | `N/A` | `N/A` | **NO MATCH (New Class)** | Candidate for V3 Expansion ('beet') |
| `3` | `bell pepper` | `18` | `capsicum` | **MATCH (Alias: bell pepper -> capsicum)** | Map to FG Class ID 18 ('capsicum') |
| `4` | `broccoli` | `21` | `broccoli` | **MATCH (Direct)** | Map to FG Class ID 21 ('broccoli') |
| `5` | `brus capusta` | `16` | `cabbage` | **MATCH (Alias: brus capusta -> cabbage)** | Map to FG Class ID 16 ('cabbage') |
| `6` | `cabbage` | `16` | `cabbage` | **MATCH (Direct)** | Map to FG Class ID 16 ('cabbage') |
| `7` | `carrot` | `15` | `carrot` | **MATCH (Direct)** | Map to FG Class ID 15 ('carrot') |
| `8` | `cayliflower` | `17` | `cauliflower` | **MATCH (Alias: cayliflower -> cauliflower)** | Map to FG Class ID 17 ('cauliflower') |
| `9` | `celery` | `N/A` | `N/A` | **NO MATCH (New Class)** | Candidate for V3 Expansion ('celery') |
| `10` | `corn` | `24` | `corn` | **MATCH (Direct)** | Map to FG Class ID 24 ('corn') |
| `11` | `cucumber` | `19` | `cucumber` | **MATCH (Direct)** | Map to FG Class ID 19 ('cucumber') |
| `12` | `eggplant` | `20` | `brinjal` | **MATCH (Alias: eggplant -> brinjal)** | Map to FG Class ID 20 ('brinjal') |
| `13` | `fasol` | `N/A` | `N/A` | **NO MATCH (New Class)** | Candidate for V3 Expansion ('fasol') |
| `14` | `garlic` | `25` | `garlic` | **MATCH (Direct)** | Map to FG Class ID 25 ('garlic') |
| `15` | `hot pepper` | `33` | `green_chilli` | **MATCH (Alias: hot pepper -> green_chilli)** | Map to FG Class ID 33 ('green_chilli') |
| `16` | `onion` | `7` | `onion` | **MATCH (Direct)** | Map to FG Class ID 7 ('onion') |
| `17` | `peas` | `23` | `peas` | **MATCH (Direct)** | Map to FG Class ID 23 ('peas') |
| `18` | `potato` | `6` | `potato` | **MATCH (Direct)** | Map to FG Class ID 6 ('potato') |
| `19` | `pumpkin` | `30` | `pumpkin` | **MATCH (Direct)** | Map to FG Class ID 30 ('pumpkin') |
| `20` | `rediska` | `29` | `radish` | **MATCH (Alias: rediska -> radish)** | Map to FG Class ID 29 ('radish') |
| `21` | `redka` | `29` | `radish` | **MATCH (Alias: redka -> radish)** | Map to FG Class ID 29 ('radish') |
| `22` | `salad` | `N/A` | `N/A` | **NO MATCH (New Class)** | Candidate for V3 Expansion ('salad') |
| `23` | `squash-patisson` | `N/A` | `N/A` | **NO MATCH (New Class)** | Candidate for V3 Expansion ('squash-patisson') |
| `24` | `tomato` | `5` | `tomato` | **MATCH (Direct)** | Map to FG Class ID 5 ('tomato') |
| `25` | `vegetable marrow` | `N/A` | `N/A` | **NO MATCH (New Class)** | Candidate for V3 Expansion ('vegetable marrow') |

## Key Indian Grocery Class Audit

| Grocery Class | Extracted Dataset Status | Extracted Annotations | FreshGuard Production Mapping |
| :--- | :--- | :--- | :--- |
| `potato` | **PRESENT** | 989 boxes | Map to FreshGuard ID `6` (`potato`) |
| `onion` | **PRESENT** | 1253 boxes | Map to FreshGuard ID `7` (`onion`) |
| `tomato` | **PRESENT** | 2298 boxes | Map to FreshGuard ID `5` (`tomato`) |
| `ginger` | **PRESENT** | 0 boxes | Map to FreshGuard ID `26` (`ginger`) |
| `garlic` | **PRESENT** | 1586 boxes | Map to FreshGuard ID `25` (`garlic`) |
| `peas` | **PRESENT** | 1025 boxes | Map to FreshGuard ID `23` (`peas`) |
| `eggplant` | **PRESENT** | 900 boxes | Map to FreshGuard ID `20` (`brinjal`) |
| `rediska` | **PRESENT** | 1179 boxes | Map to FreshGuard ID `29` (`radish`) |
| `carrot` | **PRESENT** | 1375 boxes | Map to FreshGuard ID `15` (`carrot`) |
| `hot pepper` | **PRESENT** | 1322 boxes | Map to FreshGuard ID `33` (`green_chilli`) |
| `bell pepper` | **PRESENT** | 1303 boxes | Map to FreshGuard ID `18` (`capsicum`) |
| `cucumber` | **PRESENT** | 1199 boxes | Map to FreshGuard ID `19` (`cucumber`) |
