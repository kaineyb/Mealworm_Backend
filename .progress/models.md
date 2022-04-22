# 1. Sections to Stores

## Section

**Links to `User`**

Has:

- `name` char field
- `added` datetime field

## Store Aisle

**Bridges `Store` to `Section`**

Has:

- `aisle_number` integer field

## Store

**Links to `User`**

Has:

- `name` char field
- `added` datetime field

# 2. Ingredients to Meals

## Ingredient

**Links to `Section` and `User`.**

Has a:

- `name` char field
- `added` datetime field

## Meal Ingredient

**Bridges `Ingredient` to `Meal`**

Defines:

- `unit`: Measurement of Ingredient in Items, Grams, Kilograms, Millilitres and Litres
- `quantity` of ingredient as an Integer

Has a datetime field of `added`

## Meal

**Links to `User`**

Has a `name` and a datetime `added` field

# 3. Plans to Days

## Plan

**Links `Day` and itself to a `User`**

Has a `name` and a day that the plan starts: `start_day`.

Secondary, has a datetime `last_update` and datetime `added` field.

## Day

**Links a `Plan` to a `Meal`.**

Also provides functionality for the position of the meal in the week
