exports.sum = (req, res) => {
  const { num1, num2 } = req.body;
  const parsedNum1 = parseFloat(num1);
  const parsedNum2 = parseFloat(num2);

  const result = parsedNum1 + parsedNum2;
  res.status(200).json({
    status: "success",
    data: {
      sum: result,
    },
  });
};

exports.subtract = (req, res) => {
  const { minuted, subtrahend } = req.body;
  const parsedMinuted = parseFloat(minuted);
  const parsedSubtrahend = parseFloat(subtrahend);

  const result = parsedMinuted - parsedSubtrahend;
  res.status(200).json({
    status: "success",
    data: {
      difference: result,
    },
  });
};

exports.multiply = (req, res) => {
  const { multiplier, multiplicand } = req.body;
  const parsedMultiplier = parseFloat(multiplier);
  const parsedMultiplicand = parseFloat(multiplicand);

  const result = parsedMultiplier * parsedMultiplicand;
  res.status(200).json({
    status: "success",
    data: {
      multiplication: result,
    },
  });
};

exports.divide = (req, res) => {
  const { dividend, divisor } = req.body;
  const parsedDividend = parseFloat(dividend);
  const parsedDivisor = parseFloat(divisor);

  const result = parsedDividend / parsedDivisor;
  res.status(200).json({
    status: "success",
    data: {
      division: result,
    },
  });
};
