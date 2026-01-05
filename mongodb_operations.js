/*
  FlexiMart - MongoDB Operations
  File: mongodb_operations.js

  Assumptions:
  - Database name: fleximart
  - Collection name: products
  - JSON file name: products_catalog.json
  - Each product document contains:
      product_id, name, category, price, stock, reviews:[{rating,...}], ...
*/

use("fleximart");

/* ============================================================
   Operation 1: Load Data (1 mark)
   // Import the provided JSON file into collection 'products'
   NOTE: mongosh cannot directly import a JSON file like mongoimport.
   So we provide both approaches:
   A) Recommended: mongoimport command
   B) Alternative: load() if file is valid JS array (exported)
   ============================================================ */

print("\n=== Operation 1: Load Data ===");

// A) Recommended (run in terminal, not inside mongosh):
print(`
Run this in terminal (recommended):
mongoimport --db fleximart --collection products --file products_catalog.json --jsonArray --drop
`);

// B) If you want to run inside mongosh, rename JSON to products_catalog.js
// and make sure it exports an array like: const products = [ ... ]; then:
try {
  // Uncomment below ONLY if you create products_catalog.js with: const products = [...]
  // load("./products_catalog.js");
  // db.products.drop();
  // db.products.insertMany(products);
  // print("Inserted products using load() approach.");
} catch (e) {
  // ignore if not used
}


/* ============================================================
   Operation 2: Basic Query (2 marks)
   // Find all products in "Electronics" category with price < 50000
   // Return only: name, price, stock
   ============================================================ */

print("\n=== Operation 2: Basic Query ===");

db.products.find(
  { category: "Electronics", price: { $lt: 50000 } },
  { _id: 0, name: 1, price: 1, stock: 1 }
).pretty();


/* ============================================================
   Operation 3: Review Analysis (2 marks)
   // Find all products that have average rating >= 4.0
   // Use aggregation to calculate average from reviews array
   ============================================================ */

print("\n=== Operation 3: Review Analysis (avg rating >= 4.0) ===");

db.products.aggregate([
  // If reviews might be missing, treat missing as empty array
  { $addFields: { reviews: { $ifNull: ["$reviews", []] } } },

  // Compute average rating from reviews.rating
  {
    $addFields: {
      avg_rating: { $avg: "$reviews.rating" }
    }
  },

  // Keep only products where avg_rating >= 4.0
  { $match: { avg_rating: { $gte: 4.0 } } },

  // Output fields
  {
    $project: {
      _id: 0,
      product_id: 1,
      name: 1,
      category: 1,
      avg_rating: { $round: ["$avg_rating", 2] }
    }
  },

  // Sort highest rated first
  { $sort: { avg_rating: -1 } }
]).pretty();


/* ============================================================
   Operation 4: Update Operation (2 marks)
   // Add a new review to product "ELEC001"
   // Review: {user: "U999", rating: 4, comment: "Good value", date: ISODate()}
   ============================================================ */

print("\n=== Operation 4: Add Review to ELEC001 ===");

db.products.updateOne(
  { product_id: "ELEC001" },
  {
    $push: {
      reviews: {
        user_id: "U999",
        username: "U999",
        rating: 4,
        comment: "Good value",
        date: new Date() // ISODate() equivalent in mongosh
      }
    },
    $set: {
      updated_at: new Date().toISOString()
    }
  }
);

print("Review added to ELEC001. Verify:");
db.products.find(
  { product_id: "ELEC001" },
  { _id: 0, product_id: 1, name: 1, "reviews": { $slice: -2 } }
).pretty();


/* ============================================================
   Operation 5: Complex Aggregation (3 marks)
   // Calculate average price by category
   // Return: category, avg_price, product_count
   // Sort by avg_price descending
   ============================================================ */

print("\n=== Operation 5: Average Price by Category ===");

db.products.aggregate([
  {
    $group: {
      _id: "$category",
      avg_price: { $avg: "$price" },
      product_count: { $sum: 1 }
    }
  },
  {
    $project: {
      _id: 0,
      category: "$_id",
      avg_price: { $round: ["$avg_price", 2] },
      product_count: 1
    }
  },
  { $sort: { avg_price: -1 } }
]).pretty();

print("\n All operations executed.");
