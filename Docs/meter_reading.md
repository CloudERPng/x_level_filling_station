# Meter Reading

Select a Filling Station
    - In the meter reading detail table, meters of that filling station will be fetched
    - Qty in child table corresponds to the current reading of meter
    - Rate in child table corresponds to selling rate of meter
Update New Qty against each meter
    - Sales Revenue will be calculated automatically (New Qty - Qty * Rate)
    - Total sales revenue will also be calculated automatically if sales revenue of at least one row in meter reading detail table is present
Enter Actual Total Revenue
    - Total Actual Revenue below the meter reading detail table is automatically calculated


# Mode Of Payment
Enter mode of payment and amount
Total amount must be equal to total actual revenue