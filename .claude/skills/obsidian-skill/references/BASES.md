# Bases Reference

Bases is a core plugin that creates database-like views of your notes. Data is stored
in local Markdown files and their properties. Views are described by Bases syntax,
saved as `.base` files or embedded in `base` code blocks.

## Table of Contents

1. [Creating a Base](#creating-a-base)
2. [Bases Syntax](#bases-syntax)
3. [Filters](#filters)
4. [Formulas](#formulas)
5. [Views](#views)
6. [Operators](#operators)
7. [Functions Quick Reference](#functions-quick-reference)

## Creating a Base

**Command palette:** Use `Bases: Create new base` or `Bases: Insert new base`.
**File explorer:** Right-click a folder → New base.
**Ribbon:** Select "Create new base" in the vertical ribbon menu.

### Embed a Base

Embed a `.base` file: `![[File.base]]` or `![[File.base#View]]` for a specific view.

Embed inline with a code block:

````yaml
```base
filters:
  and:
    - file.hasTag("example")
views:
  - type: table
    name: Table
```
````

## Bases Syntax

Bases are valid YAML with these top-level sections:

```yaml
filters:      # Global filters (apply to all views)
formulas:     # Calculated properties
properties:   # Display configuration
summaries:    # Custom aggregation formulas
views:        # View definitions (table, list, cards, map)
```

### Full Example

```yaml
filters:
  or:
    - file.hasTag("tag")
    - and:
        - file.hasTag("book")
        - file.hasLink("Textbook")
formulas:
  formatted_price: 'if(price, price.toFixed(2) + " dollars")'
  ppu: "(price / age).toFixed(2)"
properties:
  status:
    displayName: Status
  formula.formatted_price:
    displayName: "Price"
views:
  - type: table
    name: "My table"
    limit: 10
    groupBy:
      property: note.age
      direction: DESC
    filters:
      and:
        - 'status != "done"'
        - or:
            - "formula.ppu > 5"
            - "price > 2.1"
    order:
      - file.name
      - note.age
      - formula.ppu
    summaries:
      formula.ppu: Average
```

## Filters

By default, a base includes every file in the vault. Filters narrow the dataset.

Filters can appear at the **global** level (applies to all views) or at the
**view** level (applies only to that view). Both are concatenated with AND.

The filters section contains either a single filter string or a recursive filter
object with `and`, `or`, or `not` keys:

```yaml
filters:
  or:
    - file.hasTag("tag")
    - and:
        - file.hasTag("book")
        - file.hasLink("Textbook")
    - not:
        - file.hasTag("book")
        - file.inFolder("Required Reading")
```

Filter statements use comparison operators or functions.

## Formulas

Formulas define calculated properties displayed across all views:

```yaml
formulas:
  formatted_price: 'if(price, price.toFixed(2) + " dollars")'
  ppu: "(price / age).toFixed(2)"
```

### Referencing Properties

- **Note properties** (frontmatter): `price`, `note.price`, or `note["price"]`
- **File properties**: `file.name`, `file.size`, `file.ext`, `file.mtime`
- **Formula properties**: `formula.formatted_price`

Formulas can reference other formulas (no circular references allowed).

### Formula Examples

| Goal                   | Formula                                         |
|------------------------|-------------------------------------------------|
| Calculate deadline     | `start_date + "2w"`                             |
| Overdue status         | `if(due_date < now() && status != "Done", "Overdue", "")` |
| Format currency        | `if(price, "$" + price.toFixed(2), "")`         |
| Count list items       | `tasks.length`                                  |
| Priority score         | `(impact * urgency) / effort`                   |
| Combine text           | `first_name + " " + last_name`                  |
| Full name link         | `link(file.name, first_name + " " + last_name)` |

## Views

Each entry in `views` defines a separate view. View types: `table`, `list`,
`cards`, `map`. Community plugins can add additional layouts.

```yaml
views:
  - type: table
    name: "My table"
    limit: 10
    groupBy:
      property: note.age
      direction: DESC
    order:
      - file.name
      - note.age
    summaries:
      formula.ppu: Average
```

### Default Summary Formulas

| Name     | Input   | Description                                  |
|----------|---------|----------------------------------------------|
| Average  | Number  | Mathematical mean                            |
| Min      | Number  | Smallest number                              |
| Max      | Number  | Largest number                               |
| Sum      | Number  | Sum of all numbers                           |
| Range    | Number  | Difference between Max and Min               |
| Median   | Number  | Mathematical median                          |
| Stddev   | Number  | Standard deviation                           |
| Earliest | Date    | Earliest date                                |
| Latest   | Date    | Latest date                                  |
| Checked  | Boolean | Count of true values                         |
| Unchecked| Boolean | Count of false values                        |
| Empty    | Any     | Count of empty values                        |
| Filled   | Any     | Count of non-empty values                    |
| Unique   | Any     | Count of unique values                       |

Custom summaries use the `values` keyword (list of all values for a property):

```yaml
summaries:
  customAverage: 'values.mean().round(3)'
```

## Operators

### Arithmetic: `+`, `-`, `*`, `/`, `%`, `( )`

### Date Arithmetic

Modify dates by adding/subtracting duration strings:

```
date + "1M"           Add 1 month
date - "2h"           Subtract 2 hours
now() + "1 day"       24 hours from now
date("2024-12-01") + "1M" + "4h" + "3m"
```

Duration units: `y`/`year`/`years`, `M`/`month`/`months`, `d`/`day`/`days`,
`w`/`week`/`weeks`, `h`/`hour`/`hours`, `m`/`minute`/`minutes`, `s`/`second`/`seconds`

### Comparison: `==`, `!=`, `>`, `<`, `>=`, `<=`
### Boolean: `!` (not), `&&` (and), `||` (or)

## Functions Quick Reference

### Global Functions

| Function       | Description                                       |
|----------------|---------------------------------------------------|
| `date(str)`    | Parse string to date (`YYYY-MM-DD HH:mm:ss`)     |
| `duration(str)`| Parse string as duration                          |
| `now()`        | Current date and time                             |
| `today()`      | Current date (time set to zero)                   |
| `if(cond,t,f)` | Conditional: returns `t` if true, `f` if false    |
| `link(path,d)` | Create a link object (optional display text `d`)  |
| `image(path)`  | Render an image                                   |
| `icon(name)`   | Render a Lucide icon                              |
| `file(path)`   | Get file object by path                           |
| `html(str)`    | Render string as HTML                             |
| `list(elem)`   | Wrap element in list (or return list unchanged)   |
| `number(val)`  | Convert value to number                           |
| `max(a,b,...)`  | Largest of provided numbers                       |
| `min(a,b,...)`  | Smallest of provided numbers                      |
| `escapeHTML(s)` | Escape HTML special characters                    |

### String Functions

`contains()`, `containsAll()`, `containsAny()`, `startsWith()`, `endsWith()`,
`lower()`, `title()`, `trim()`, `replace(pattern, replacement)`, `split(sep, n)`,
`slice(start, end)`, `repeat(count)`, `reverse()`, `isEmpty()`, `.length`

### Number Functions

`abs()`, `ceil()`, `floor()`, `round(digits)`, `toFixed(precision)`, `isEmpty()`

### Date Functions

Fields: `.year`, `.month`, `.day`, `.hour`, `.minute`, `.second`, `.millisecond`
Methods: `date()` (remove time), `time()`, `format(str)`, `relative()`, `isEmpty()`

### List Functions

`contains()`, `containsAll()`, `containsAny()`, `filter(expr)`, `map(expr)`,
`reduce(expr, acc)`, `sort()`, `reverse()`, `unique()`, `flat()`, `join(sep)`,
`slice(start, end)`, `isEmpty()`, `.length`

### File Functions/Fields

Fields: `file.name`, `file.basename`, `file.path`, `file.folder`, `file.ext`,
`file.size`, `file.ctime`, `file.mtime`, `file.tags`, `file.links`, `file.properties`

Methods: `hasTag(tags...)`, `hasLink(file)`, `hasProperty(name)`, `inFolder(folder)`,
`asLink(display?)`

### Link Functions

`asFile()`, `linksTo(file)`

### The `this` Object

- In main content area: refers to the base file itself
- Embedded in another file: refers to the embedding file
- In sidebar: refers to the active file in the main content area

Example: `file.hasLink(this.file)` replicates the backlinks pane.

## Property Types in Bases

Three kinds of properties:

1. **Note properties** — frontmatter (`author` or `note.author`)
2. **File properties** — file metadata (`file.name`, `file.size`, `file.mtime`)
3. **Formula properties** — defined in the `.base` file (`formula.price_per_unit`)
