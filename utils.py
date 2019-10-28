def sum_tuples(*tuples):
    return list(
        sum([tup[i] for tup in tuples])
        for i, t in enumerate(tuples[0])
    )


if __name__ == '__main__':
    print(
        sum_tuples(*[
            (1., 2, 3, 4),
            (1, 2., 3, 4),
            (1, 2, 3., 4),
            (1, 2, 3, 4.),
        ])
    )