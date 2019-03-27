- [x] Empty lines
- [x] Comment handling to refactor
- [x] Empty facts crashes:
    ```
    A => B
    =
    ?B
    ```
- [x] Join facts/questions works but does not assign computed value well. (parse:parse_tab:18) It should return value and main should change tab value.
- [ ] Parenthesis handling to FIX.
- [ ] why trailing space in dic rules ? `rules:  {'B': 'C '}`
- [ ] doesnt handle same conclusions :
    ```
    input : - ['A => B', 'C => B', '=A', '?B']
    rules:  {'B': 'C '}
    query:  B
    facts:  A
    ```
- [ ] ds