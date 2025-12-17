const fs = require('fs');
const { parse } = require('json2csv');

function main(params) {
  // Extract transaction data
  const transaction = params.data;
  const network = params.metadata?.network || 'optimism';

  // Basic transformation
  const processedData = {
    transaction_hash: transaction.transactionHash,
    from_address: transaction.from,
    to_address: transaction.to,
    value: parseFloat(transaction.value),   // or parse based on your needs
    network,
    timestamp: transaction.timestamp
  };

  // Convert data to CSV format
  const csv = parse([processedData]);

  // Define CSV file path
  const filePath = 'transaction_data.csv';

  // Write CSV to file
  fs.appendFile(filePath, csv + '\n', (err) => {
    if (err) {
      console.error('Error writing to CSV file:', err);
    } else {
      console.log('Data successfully exported to CSV!');
    }
  });

  return { message: "Data processed and exported to CSV." };
}
