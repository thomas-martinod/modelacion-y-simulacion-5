library(readxl)
library(lubridate)

df <- read_excel("C:\\Users\\thomm\\Documents\\GitHub\\modelacion-y-simulacion-5\\proyecto-final-prebel\\bases-de-datos\\datos-discretos.xlsx")

# Initialize an empty vector for orders
orders <- c()

# Loop through each element in df$Orden
for (i in df$Orden) {
  if (!(i %in% orders)) {
    orders <- c(orders, i)
  }
}

# Get the length of the orders vector
orders_length <- length(orders)

# Initialize vectors to store max and min date-times
max_time <- rep(NA, orders_length)
min_time <- rep(NA, orders_length)

# Iterate over each order
for (j in 1:orders_length) {
  order <- orders[j]
  
  # Filter rows for the current order
  order_indices <- which(df$Orden == order)
  
  # Extract the corresponding date-times and parse them
  order_datetimes <- mdy_hms(df$`Fecha Inicio`[order_indices], tz = "America/Bogota")
  
  # Find the max and min date-times
  max_time[j] <- max(order_datetimes, na.rm = TRUE)
  min_time[j] <- min(order_datetimes, na.rm = TRUE)
}

# Print the results
print(max_time)
print(min_time)

# Optionally, convert to character to see the formatted output
print(as.character(max_time))
print(as.character(min_time))
