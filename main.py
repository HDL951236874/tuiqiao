from N_gram import N_gram

if __name__ == '__main__':
    BeforeCorrect = '今添田气不好。'
    Model = N_gram()
    AfterCorrector = Model.correct_single_sen(BeforeCorrect)
    print(AfterCorrector)
