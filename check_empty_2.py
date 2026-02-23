import os
import ast

directories = [
    "src/domains/customers/lambdas/get_customers",
    "src/domains/customers/lambdas/get_customer_by_id",
    "src/domains/customers/lambdas/add_customer",
    "src/domains/customers/lambdas/update_customer",
    "src/domains/customers/lambdas/delete_customer",
    "src/domains/repairs/lambdas/get_repairs",
    "src/domains/repairs/lambdas/get_repair_by_id",
    "src/domains/repairs/lambdas/add_repair",
    "src/domains/repairs/lambdas/update_repair",
    "src/domains/repairs/lambdas/delete_repair",
    "src/domains/mechanics/lambdas/get_mechanics",
    "src/domains/mechanics/lambdas/get_mechanic_by_id",
    "src/domains/mechanics/lambdas/add_mechanic",
    "src/domains/mechanics/lambdas/update_mechanic",
    "src/domains/mechanics/lambdas/delete_mechanic",
    "src/domains/products/lambdas/get_products",
    "src/domains/products/lambdas/get_product_by_id",
    "src/domains/products/lambdas/add_product",
    "src/domains/products/lambdas/update_product",
    "src/domains/products/lambdas/delete_product",
    "src/domains/cashboxes/lambdas/get_cashbox",
    "src/domains/cashboxes/lambdas/get_current_session",
    "src/domains/cashboxes/lambdas/add_cashbox",
    "src/domains/cashboxes/lambdas/open_cashbox",
    "src/domains/cashboxes/lambdas/close_cashbox",
    "src/domains/dashboard_datas/lambdas/get_dashboard",
    "src/domains/bulk_products/lambdas/add_products",
    "src/domains/suppliers/lambdas/get_suppliers",
    "src/domains/suppliers/lambdas/get_supplier_by_id",
    "src/domains/suppliers/lambdas/add_supplier",
    "src/domains/suppliers/lambdas/update_supplier",
    "src/domains/suppliers/lambdas/delete_supplier",
    "src/domains/sales/lambdas/get_sales",
    "src/domains/sales/lambdas/get_sale_by_id",
    "src/domains/sales/lambdas/add_sale",
    "src/domains/sales/lambdas/update_sale",
    "src/domains/sales/lambdas/delete_sale",
    "src/domains/sales/lambdas/get_payment_methods",
]

for d in directories:
    if not os.path.exists(d):
        print(f"Directory missing: {d}")
        continue
    
    main_py_path = os.path.join(d, 'main.py')
    if not os.path.exists(main_py_path):
        print(f"Missing main.py: {main_py_path}")
    else:
        with open(main_py_path, 'r', encoding='utf-8') as f:
            content = f.read()
            # check if body is just pass or return something empty
            # look for lambda_handler
            if 'def lambda_handler' not in content:
                print(f"Missing lambda_handler in {main_py_path}")
            elif 'return None' in content or 'return {}' in content or 'NotImplemented' in content:
                print(f"Potentially incomplete implementation in {main_py_path}")
                
