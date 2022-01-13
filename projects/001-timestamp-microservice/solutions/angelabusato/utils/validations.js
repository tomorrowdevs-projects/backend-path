/**
 * Checks if the date parameter is a valid Date
 * @param {Date} date
 * @returns Boolean
 */
const isValidDate = (date) => {
  return date instanceof Date && !isNaN(date);
};

module.exports = isValidDate;
