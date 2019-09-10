from tuiqiao.N_gram import N_gram

if __name__ == '__main__':
    Model = N_gram()
    train_res = Model.PROCESS()
    Model.save_model(train_res)


