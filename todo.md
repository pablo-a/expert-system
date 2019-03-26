- [x] Empty lines
- [ ] why trailing space in dic rules ? `rules:  {'B': 'C '}`
- [ ] doesnt handle same conclusions :
    ```
    input : - ['A => B', 'C => B', '=A', '?B']
    rules:  {'B': 'C '}
    query:  B
    facts:  A
    ```
- [x] Comment handling to refactor
- [ ] Parenthesis handling to FIX.
- [ ] Empty facts crashes:
    ```
    A => B
    =
    ?B
    ```
- [ ] Join facts/questions works but does not assign computed value well. (parse:parse_tab:18) It should return value and main should change tab value.
- [ ] ds