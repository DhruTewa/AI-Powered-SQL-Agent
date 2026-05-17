TABLE_DESCRIPTIONS = {

    # ── Human Resources ───────────────────────────────────────────────────────
    "humanresources.department": (
        "Company departments and their group categories such as Engineering, Sales and Marketing"
    ),
    "humanresources.employee": (
        "Employee records including job title, hire date, gender, marital status and national ID"
    ),
    "humanresources.employeedepartmenthistory": (
        "History of which department and shift each employee has worked in over time"
    ),
    "humanresources.employeepayhistory": (
        "Historical pay rate changes for each employee including pay frequency"
    ),
    "humanresources.jobcandidate": (
        "Job applicants who submitted resumes, may or may not have been hired as employees"
    ),
    "humanresources.shift": (
        "Work shifts available at the company including start and end times"
    ),
    "humanresources.vemployee": (
        "Pre-joined view of employee details including full name, job title, phone number and address"
    ),
    "humanresources.vemployeedepartment": (
        "Pre-joined view of employees with their current department and shift assignment"
    ),
    "humanresources.vemployeedepartmenthistory": (
        "Pre-joined view of employees with full history of department and shift changes"
    ),
    "humanresources.vjobcandidate": (
        "Pre-joined view of job candidates with personal details extracted from their resume"
    ),
    "humanresources.vjobcandidateeducation": (
        "Education history extracted from job candidate resumes including degree and institution"
    ),
    "humanresources.vjobcandidateemployment": (
        "Employment history extracted from job candidate resumes including job title and organisation"
    ),

    # ── Person ────────────────────────────────────────────────────────────────
    "person.address": (
        "Physical addresses including street, city, state and postal code used by customers, employees and vendors"
    ),
    "person.addresstype": (
        "Types of addresses such as Home, Billing and Shipping used to classify address records"
    ),
    "person.businessentity": (
        "Root table for all entities in the system — every person, store and vendor has a record here"
    ),
    "person.businessentityaddress": (
        "Links business entities to their addresses with the type of address"
    ),
    "person.businessentitycontact": (
        "Links people to organisations as contacts with a defined contact role"
    ),
    "person.contacttype": (
        "Types of contact roles such as Owner, Sales Agent and Purchasing Manager"
    ),
    "person.countryregion": (
        "Country and region codes used for addresses and sales territories"
    ),
    "person.emailaddress": (
        "Email addresses associated with people including customers and employees"
    ),
    "person.password": (
        "Hashed passwords for customer online accounts"
    ),
    "person.person": (
        "All people in the system including customers, employees and vendor contacts with full name and personal details"
    ),
    "person.personphone": (
        "Phone numbers associated with people including the type of phone such as Cell, Work or Home"
    ),
    "person.phonenumbertype": (
        "Types of phone numbers such as Cell, Work and Home"
    ),
    "person.stateprovince": (
        "States and provinces with country codes used for addresses and tax rates"
    ),
    "person.vadditionalcontactinfo": (
        "Pre-joined view of additional contact information for people including phone and address details"
    ),

    # ── Production ────────────────────────────────────────────────────────────
    "production.billofmaterials": (
        "Components and sub-assemblies required to manufacture each product including quantities and valid dates"
    ),
    "production.culture": (
        "Languages and cultures used for product descriptions such as English, French and Chinese"
    ),
    "production.document": (
        "Internal company documents related to products and manufacturing processes"
    ),
    "production.illustration": (
        "Diagrams and illustrations used in product manufacturing instructions"
    ),
    "production.location": (
        "Manufacturing locations and work centres with hourly cost rates and available capacity"
    ),
    "production.product": (
        "All products sold or manufactured by the company including name, price, colour, stock levels and category"
    ),
    "production.productcategory": (
        "Top-level product categories such as Bikes, Clothing, Accessories and Components"
    ),
    "production.productcosthistory": (
        "Historical standard manufacturing cost changes for each product over time"
    ),
    "production.productdescription": (
        "Text descriptions of products available in multiple languages"
    ),
    "production.productdocument": (
        "Links products to their related internal documents"
    ),
    "production.productinventory": (
        "Current stock quantity for each product at each warehouse or manufacturing location"
    ),
    "production.productlistpricehistory": (
        "Historical list price changes for each product showing when prices were raised or lowered"
    ),
    "production.productmodel": (
        "Product model templates that group related products with catalog descriptions and build instructions"
    ),
    "production.productmodelillustration": (
        "Links product models to their manufacturing diagrams and illustrations"
    ),
    "production.productmodelproductdescriptionculture": (
        "Links product models to their descriptions in specific languages and cultures"
    ),
    "production.productphoto": (
        "Product photos stored in thumbnail and full size formats"
    ),
    "production.productproductphoto": (
        "Links products to their photos"
    ),
    "production.productreview": (
        "Customer reviews and star ratings submitted for products"
    ),
    "production.productsubcategory": (
        "Sub-categories under the main product categories such as Mountain Bikes and Road Bikes under Bikes"
    ),
    "production.scrapreason": (
        "Reasons why manufactured products were scrapped or rejected during production"
    ),
    "production.transactionhistory": (
        "Recent inventory transactions including purchases, sales and work orders with quantities and costs"
    ),
    "production.transactionhistoryarchive": (
        "Archived historical inventory transactions moved from the main transaction history table"
    ),
    "production.unitmeasure": (
        "Units of measurement used for products and bill of materials such as Each, Pound and Hour"
    ),
    "production.vproductmodelcatalogdescription": (
        "Pre-joined view of product models with full catalog descriptions, warranty information and product URL"
    ),
    "production.vproductmodelinstructions": (
        "Pre-joined view of product models with manufacturing instructions and time estimates per work centre"
    ),
    "production.workorder": (
        "Manufacturing work orders for producing products including planned quantities, start and end dates"
    ),
    "production.workorderrouting": (
        "Routing steps and scheduled times for each manufacturing work order across work centres"
    ),

    # ── Purchasing ────────────────────────────────────────────────────────────
    "purchasing.productvendor": (
        "Which vendors supply which products including lead time, standard price and minimum and maximum order quantities"
    ),
    "purchasing.purchaseorderdetail": (
        "Individual product line items on purchase orders with quantity, unit price and received quantity"
    ),
    "purchasing.purchaseorderheader": (
        "Purchase orders placed with vendors including order date, ship date, status and total due"
    ),
    "purchasing.shipmethod": (
        "Shipping methods available for purchase orders including base shipping cost and per-unit rate"
    ),
    "purchasing.vendor": (
        "Suppliers and vendors used for purchasing products with credit rating, preferred status and contact details"
    ),
    "purchasing.vvendorwithaddresses": (
        "Pre-joined view of vendors with their full address details including city and state"
    ),
    "purchasing.vvendorwithcontacts": (
        "Pre-joined view of vendors with their contact person names and roles"
    ),

    # ── Sales ─────────────────────────────────────────────────────────────────
    "sales.countryregioncurrency": (
        "Maps countries and regions to their currencies for international sales"
    ),
    "sales.creditcard": (
        "Credit card details used by customers for purchases including card type and expiry date"
    ),
    "sales.currency": (
        "Currency codes and names used in sales transactions"
    ),
    "sales.currencyrate": (
        "Daily currency exchange rates between currencies used for international orders"
    ),
    "sales.customer": (
        "Customer accounts linking people and stores to their sales territory"
    ),
    "sales.personcreditcard": (
        "Links individual customers to their registered credit cards"
    ),
    "sales.salesorderdetail": (
        "Individual product line items on sales orders including product, quantity, unit price and discount"
    ),
    "sales.salesorderheader": (
        "Sales orders with customer details, order date, ship date, status and total amount due"
    ),
    "sales.salesorderheadersalesreason": (
        "Links sales orders to the reasons why the customer made the purchase"
    ),
    "sales.salesperson": (
        "Sales representatives with their assigned territory, sales quota, bonus and year-to-date sales totals"
    ),
    "sales.salespersonquotahistory": (
        "Historical sales quota targets assigned to each sales representative by quarter"
    ),
    "sales.salesreason": (
        "Reasons why customers made purchases such as Price, Quality and Magazine Advertisement"
    ),
    "sales.salestaxrate": (
        "Tax rates applied to sales by state and province including tax type and rate percentage"
    ),
    "sales.salesterritory": (
        "Sales territories grouped by region with year-to-date sales revenue and cost figures"
    ),
    "sales.salesterritoryhistory": (
        "History of which sales territory each sales representative has been assigned to over time"
    ),
    "sales.shoppingcartitem": (
        "Products currently sitting in customer online shopping carts awaiting checkout"
    ),
    "sales.specialoffer": (
        "Promotional discounts and special offers available for products including discount percentage and valid dates"
    ),
    "sales.specialofferproduct": (
        "Links special offers to the specific products they apply to"
    ),
    "sales.store": (
        "Retail store customers with business demographics, annual sales figures and assigned sales representative"
    ),
    "sales.vindividualcustomer": (
        "Pre-joined view of individual non-store customers with full name, phone number and address"
    ),
    "sales.vpersondemographics": (
        "Pre-joined view of customer purchasing demographics including yearly income, total purchases and first purchase date"
    ),
    "sales.vsalesperson": (
        "Pre-joined view of sales representatives with full contact details, job title and territory"
    ),
    "sales.vsalespersonsalesbyfiscalyears": (
        "Pre-joined pivot view of sales totals per sales representative broken down by fiscal year"
    ),
    "sales.vsalespersonsalesbyfiscalyearsdata": (
        "Underlying row-level data for sales by fiscal year used to generate the fiscal year pivot view"
    ),
    "sales.vstorewithaddresses": (
        "Pre-joined view of store customers with their full address details"
    ),
    "sales.vstorewithcontacts": (
        "Pre-joined view of store customers with their contact person names and roles"
    ),
    "sales.vstorewithdemographics": (
        "Pre-joined view of store customers with business demographics including annual sales, revenue and business type"
    ),
}
