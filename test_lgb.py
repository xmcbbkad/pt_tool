import lightgbm as lgb
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

# 加载数据集
iris = datasets.load_iris()
X = iris.data
y = iris.target

# 将问题简化为二分类问题
X = X[y != 2]
y = y[y != 2]

# 划分训练集和测试集
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# 创建一个LightGBM数据格式的实例
train_data = lgb.Dataset(X_train, label=y_train)
test_data = lgb.Dataset(X_test, label=y_test)

# 设置参数
params = {
    'boosting_type': 'gbdt',
    'objective': 'binary',
    'metric': 'binary_logloss',
    'num_leaves': 31,
    'learning_rate': 0.05,
    'feature_fraction': 0.9,
    'bagging_fraction': 0.8,
    'bagging_freq': 5,
    'verbose': 0
}

# 训练模型
gbm = lgb.train(params,
                train_set=train_data,
                valid_sets=[test_data],
                num_boost_round=100,
                callbacks=[lgb.early_stopping(stopping_rounds=10)])

# 预测测试集
y_pred = gbm.predict(X_test, num_iteration=gbm.best_iteration)
y_pred_class = (y_pred >= 0.5).astype(int)

# 计算准确率
accuracy = accuracy_score(y_test, y_pred_class)
print(f'Accuracy: {accuracy:.2f}')
