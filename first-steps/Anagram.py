def is_anagram(s1,s2):
    s1 = sorted(s1)
    s2 = sorted(s2)
    return s1 == s2

def anagrams(s):
    w = list(set(s.split()))
    d = {}
    for i in range(len(w)):
        s = ''.join(sorted(w[i]))
        if s in d:
            d[s].append(i)
        else:
            d[s] = [i]

    result = []
    for s in d:
        if len(d[s]) > 1:
            result.append([w[i] for i in d[s]])

    return result

if __name__ == '__main__':
    print("%s vs %s : %i" % ("chien", "chine", is_anagram("chien", "chine")))
    print("%s vs %s : %i" % ("charme", "marche", is_anagram("charme", "marche")))
    print("%s vs %s : %i" % ("chien", "marche", is_anagram("chien", "marche")))

    print(anagrams("le chien marche vers sa niche et trouve une limace de chine nue pleine de malice qui lui fait du charme"))