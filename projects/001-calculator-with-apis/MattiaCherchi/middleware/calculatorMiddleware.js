exports.sum = (req, res) => {
  const { num1, num2 } = req.body;

  const result = (num1 + num2).toFixed(2);
  res.status(200).json({
    status: "success",
    data: {
      sum: result,
    },
  });
};

exports.subtract = (req, res) => {
  const { minuted, subtrahend } = req.body;
  const result = (minuted - subtrahend).toFixed(2);
  res.status(200).json({
    status: "success",
    data: {
      difference: result,
    },
  });
};

exports.multiply = (req, res) => {
  const { multiplier, multiplicand } = req.body;
  const result = (multiplier * multiplicand).toFixed(2);
  res.status(200).json({
    status: "success",
    data: {
      multiplication: result,
    },
  });
};

exports.divide = (req, res) => {
  const { dividend, divisor } = req.body;
  const result = (dividend / divisor).toFixed(2);
  res.status(200).json({
    status: "success",
    data: {
      division: result,
    },
  });
};
