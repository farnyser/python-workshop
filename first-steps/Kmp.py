import timeit


def find_pattern(t, s):
    """ Naive implementation """
    for i in range(len(t) - len(s) + 1):
        if t[i:i + len(s)] == s:
            return i
    return None


def find_pattern_kmp_all_in_one(t, s):
    """ Knuth Morris Pratt """

    r = [0] * len(s)
    j = r[0] = -1

    for i in range(1, len(s)):
        while j >= 0 and s[i - 1] != s[j]:
            j = r[j]
        j += 1
        r[i] = j

    j = 0
    for i in range(len(t)):
        while j >= 0 and t[i] != s[j]:
            j = r[j]
        j += 1
        if j == len(s):
            return i - len(s) + 1

    return None


def build_kmp_table(s):
    """ Knuth Morris Pratt Table """
    r = [0] * len(s)
    pos = 1
    cnd = 0
    r[0] = -1

    while pos < len(s):
        if s[pos] == s[cnd]:
            r[pos] = r[cnd]
            pos += 1
            cnd += 1
        else:
            r[pos] = cnd
            cnd = r[cnd]
            while cnd >= 0 and r[pos] != r[cnd]:
                cnd = r[cnd]
            pos += 1
            cnd += 1

    return r


def find_pattern_kmp(t, s, r):
    """ Knuth Morris Pratt Search """
    j = 0
    for i in range(len(t)):
        while j >= 0 and t[i] != s[j]:
            j = r[j]
        j += 1
        if j == len(s):
            return i - len(s) + 1

    return None


if __name__ == '__main__':
    t1 = "lallaulilalolalalilllu";
    t2 = "lallaulilalolalalillalilollalalolalalallu" * 10 + "lolalolalola"

    print(find_pattern(t1, "lilu"))
    print(find_pattern_kmp(t1, "lilu", build_kmp_table("lilu")))

    print(find_pattern(t1, "lala"))
    print(find_pattern_kmp(t1, "lala", build_kmp_table("lala")))

    print(find_pattern(t2, "lolalolalola"))
    print(find_pattern_kmp(t2, "lolalolalola", build_kmp_table("lolalolalola")))

    naive = timeit.timeit('find_pattern("lallaulilalolalalilllu","lilu")', setup="from __main__ import find_pattern",
                          number=100000);
    print("naive (not found): %fs" % (naive))

    kmp = timeit.timeit('find_pattern_kmp("lallaulilalolalalilllu","lilu", r)',
                        setup="from __main__ import find_pattern_kmp, build_kmp_table; r = build_kmp_table('lilu')",
                        number=100000);
    print("kmp (not found): %fs" % (kmp))

    naive = timeit.timeit('find_pattern("lallaulilalolalalilllu","lala")', setup="from __main__ import find_pattern",
                          number=100000);
    print("naive (simple pattern): %fs" % (naive))

    kmp = timeit.timeit('find_pattern_kmp("lallaulilalolalalilllu","lala", r)',
                        setup="from __main__ import find_pattern_kmp, build_kmp_table; r = build_kmp_table('lala')",
                        number=100000);
    print("kmp (simple pattern): %fs" % (kmp))

    naive = timeit.timeit(
        'find_pattern("lallaulilalolalalillalilollalalolalalallu" * 10 + "lolalolalola","lolalolalola")',
        setup="from __main__ import find_pattern",
        number=100000);
    print("naive (long pattern): %fs" % (naive))

    kmp = timeit.timeit(
        'find_pattern_kmp("lallaulilalolalalillalilollalalolalalallu" * 10 + "lolalolalola","lolalolalola", r)',
        setup="from __main__ import find_pattern_kmp, build_kmp_table; r = build_kmp_table('lolalolalola')",
        number=100000);
    print("kmp (long pattern): %fs" % (kmp))
