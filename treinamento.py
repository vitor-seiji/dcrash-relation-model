# Preparar features
colunas_remover = ["ID", "data", "latitude", "longitude", "fatalidades", "concessionaria", "sentido", "severidade", "fatores_agravantes"]
X = pd.get_dummies(df.drop(columns=colunas_remover, errors='ignore'), drop_first=True)
y = df['severidade']

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

print(f"\nTreinando: {X_train.shape[0]:,} | Teste: {X_test.shape[0]:,} | Features: {X.shape[1]}")

modelo = GradientBoostingClassifier(n_estimators=500, learning_rate=0.1, max_depth=6, random_state=42)
modelo.fit(X_train, y_train)

# Predições e métricas
y_pred = modelo.predict(X_test)
y_pred_proba = modelo.predict_proba(X_test)
acc = accuracy_score(y_test, y_pred)
balanced_acc = balanced_accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred, target_names=labels, output_dict=True, zero_division=0)
cm = confusion_matrix(y_test, y_pred)
