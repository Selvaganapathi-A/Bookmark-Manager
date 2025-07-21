def get_column_names(table):
    cols = list(table.columns)
    # print(dir(cols[0]))
    print(f'class {table.name}ModelDict(TypedDict):')
    set_optional: bool = True

    for col in cols:
        if col.primary_key or col.nullable:
            set_optional = True
        else:
            set_optional = False
        col_type = col.type.python_type.__name__
        if (set_optional and col.primary_key) or col.doc == 'NotRequired':
            print(f'\t{col.name}: NotRequired[Optional[{col_type}]]'.expandtabs(
                4))
        elif set_optional:
            print(f'\t{col.name}: Optional[{col_type}]'.expandtabs(4))
        else:
            print(f'\t{col.key}: {col_type}'.expandtabs(4))
        # print(f'\t# {col.doc}'.expandtabs(4))

    print()
    # print(f'\t### {dir(col.type)!r}')
    print()
