def test_extract_features():
    transaction = Transaction(amount=100.0, time=200.0, type="purchase", account_id=1, location="US")
    features = extract_features(transaction)
    assert features.shape == (1, 5)

def test_get_model_valid():
    model = get_model("random_cut_forest")
    assert model is not None

def test_make_prediction():
    model = get_model("xgboost")
    features = np.array([[100.0, 200.0, "purchase", 1, "US"]])
    prediction = make_prediction(model, features)
    assert isinstance(prediction, np.ndarray)
