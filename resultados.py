fig, axes = plt.subplots(2, 2, figsize=(15, 10))
colors = ['#2ecc71', '#f39c12', '#e74c3c']

# 1. Matriz de Confusão
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', xticklabels=labels, yticklabels=labels, ax=axes[0,0])
axes[0,0].set_title('Matriz de Confusão', fontweight='bold')

# 2. Métricas por Classe
metrics_data = [[report[c]['precision'], report[c]['recall'], report[c]['f1-score']] for c in labels if c in report]
metrics_df = pd.DataFrame(metrics_data, columns=['Precisão', 'Recall', 'F1'], index=labels)
x = np.arange(len(labels))
w = 0.25
for i, col in enumerate(['Precisão', 'Recall', 'F1']):
    axes[0,1].bar(x + i*w, metrics_df[col], w, label=col, alpha=0.8)
axes[0,1].set_xticks(x + w)
axes[0,1].set_xticklabels(labels)
axes[0,1].set_title('Métricas por Classe', fontweight='bold')
axes[0,1].legend()
axes[0,1].grid(axis='y', alpha=0.3)

# 3. Distribuição de Classes
class_counts = df['severidade'].value_counts().sort_index()
bars = axes[1,0].bar(labels, class_counts.values, color=colors, alpha=0.7)
for bar, count in zip(bars, class_counts.values):
    height = bar.get_height()
    axes[1,0].text(bar.get_x() + bar.get_width()/2., height + class_counts.max() * 0.01,
                  f'{count:,}\n({count/class_counts.sum()*100:.1f}%)', ha='center', va='bottom', fontweight='bold')
axes[1,0].set_title('Distribuição das Classes', fontweight='bold')
axes[1,0].grid(axis='y', alpha=0.3)

# 4. Top 10 Features
importances = modelo.feature_importances_
indices = np.argsort(importances)[::-1][:10]
top_features = [X.columns[i] for i in indices]
top_importances = importances[indices]
axes[1,1].barh(range(len(top_features)), top_importances, alpha=0.7)
axes[1,1].set_yticks(range(len(top_features)))
axes[1,1].set_yticklabels([f.replace('_', ' ').title() for f in reversed(top_features)])
axes[1,1].set_title('Top 10 Features', fontweight='bold')
axes[1,1].grid(axis='x', alpha=0.3)

plt.tight_layout()
plt.show()

# Gráfico de Confiança
fig, axes = plt.subplots(1, 2, figsize=(14, 5))

# Distribuição de Probabilidades
for i, classe in enumerate(labels):
    axes[0].hist(y_pred_proba[:, i], bins=20, alpha=0.6, label=classe, color=colors[i])
axes[0].set_title('Distribuição das Probabilidades', fontweight='bold')
axes[0].legend()
axes[0].grid(alpha=0.3)

# Confiança das Predições
max_probs = np.max(y_pred_proba, axis=1)
axes[1].hist(max_probs, bins=20, alpha=0.7, color='skyblue')
axes[1].axvline(np.mean(max_probs), color='red', linestyle='--', label=f'Média: {np.mean(max_probs):.3f}')
axes[1].set_title('Confiança das Predições', fontweight='bold')
axes[1].legend()
axes[1].grid(alpha=0.3)

plt.tight_layout()
plt.show()
