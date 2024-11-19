import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the datasets
category_df = pd.read_csv('dataset/product_category_name_translation.csv')
sellers_df = pd.read_csv('dataset/olist_sellers_dataset.csv')
products_df = pd.read_csv('dataset/olist_products_dataset.csv')
order_payments_df = pd.read_csv('dataset/olist_order_payments_dataset.csv')
customers_df = pd.read_csv('dataset/olist_customers_dataset.csv')
order_reviews_df = pd.read_csv('dataset/olist_order_reviews_dataset.csv')
order_items_df = pd.read_csv('dataset/olist_order_items_dataset.csv')
orders_df = pd.read_csv('dataset/olist_orders_dataset.csv')
geolocation_df = pd.read_csv('dataset/olist_geolocation_dataset.csv')

# Merge product data with categories
products_with_category = pd.merge(products_df, category_df, on='product_category_name', how='left')

# Merge orders with order items
merged_orders_items = pd.merge(orders_df, order_items_df, on='order_id', how='inner')

# Now, merge the product data (with category information) into merged_orders_items
merged_orders_items_with_category = pd.merge(merged_orders_items, products_with_category[['product_id', 'product_category_name_english']], on='product_id', how='left')

# Check the column names of the merged data to confirm the presence of 'product_category_name_english'
print("Columns in merged_orders_items_with_category:")
print(merged_orders_items_with_category.columns)

# Count the number of products sold per category
sales_by_category = merged_orders_items_with_category.groupby('product_category_name_english').size().reset_index(name='sales_count')

# Sort the data by sales count in descending order
sales_by_category_sorted = sales_by_category.sort_values('sales_count', ascending=False)

# Visualization: Sales by Category
plt.figure(figsize=(12, 8))
sns.set(style="whitegrid")  # Set a clean background for the plot
sns.barplot(x='sales_count', y='product_category_name_english', data=sales_by_category_sorted, palette='viridis', hue='product_category_name_english', legend=False)

# Rotate the category names for better readability
plt.xticks(rotation=45, ha='right')

# Add titles and labels
plt.title('Sales by Product Category', fontsize=16)
plt.xlabel('Number of Sales', fontsize=12)
plt.ylabel('Product Category', fontsize=12)

# Show the plot
plt.tight_layout()  # Ensure the layout fits without cutting off labels
plt.show()

# Save the results to CSV
sales_by_category_sorted.to_csv('sales_by_category.csv', index=False)

print("\nAnalysis complete and results saved as CSV.")
