export type Page = "Dashboard" | "Products & Stock" | "Sales" | "Purchases" | "Contacts" | "Expenses" | "Branches" | "Reports" | "Settings";
export type ContactKind = "Customer" | "Supplier" | "Both";
export interface Product {
  id: string; sku: string; name: string; category: string; unit: string;
  reorderLevel: number; sellingPrice: number; costPrice: number; active: boolean;
  createdAt: string;
}
export interface Batch {
  id: string; productId: string; batchNumber: string; quantity: number;
  manufacturingDate: string; expiryDate: string; receivedAt: string; branchId: string;
}
export interface Contact {
  id: string; name: string; kind: ContactKind; phone: string; email: string;
  address: string; openingBalance: number; createdAt: string;
}
export interface LineItem { productId: string; quantity: number; unitPrice: number; batchId?: string; }
export interface Sale {
  id: string; invoiceNumber: string; date: string; customerId: string;
  items: LineItem[]; subtotal: number; discount: number; total: number;
  amountPaid: number; paymentMethod: string; status: "Paid" | "Part-paid" | "Credit";
  branchId: string; notes: string;
}
export interface Purchase {
  id: string; purchaseNumber: string; date: string; supplierId: string;
  items: LineItem[]; subtotal: number; total: number; amountPaid: number;
  paymentMethod: string; status: "Paid" | "Part-paid" | "Credit"; branchId: string; notes: string;
}
export interface Expense {
  id: string; date: string; category: string; description: string; amount: number;
  paymentMethod: string; branchId: string;
}
export interface Branch { id: string; name: string; code: string; address: string; active: boolean; }
export interface AppData {
  products: Product[]; batches: Batch[]; contacts: Contact[]; sales: Sale[];
  purchases: Purchase[]; expenses: Expense[]; branches: Branch[];
}
