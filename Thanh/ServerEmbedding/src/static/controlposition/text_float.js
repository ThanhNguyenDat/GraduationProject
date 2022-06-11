
const {check} = require('express-validator')
const repo = require('./repository')
module.exports = {
   
  validateInterestRate : check('irate')
 
    // To delete leading and trailing space
    .trim()
 
    // Converting to float
    .toFloat()
 
    // Validate interest rate to accept
    // only float number
    .isFloat()
 
    // Custom message
    .withMessage('Must be a float number')  
}