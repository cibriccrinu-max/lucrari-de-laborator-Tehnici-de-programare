# test_diferenta.py - verifica faptul cheie: iese doar ce e nou
def test_doar_ce_e_nou():
    acum = {"a", "b", "c"}
    baza = {"a", "b"}
    assert acum - baza == {"c"}
