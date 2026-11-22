import datetime
from pathlib import Path

import OrcaWork

GOLDEN = Path(__file__).parent / "golden"
FECHA = datetime.datetime(2020, 11, 2)
DATOS = dict(
    Nombre_trabajo="prueba",
    Numero_nucleos="8",
    Nucleos_nodo="4",
    Modulo="test",
    Metodo="B3LYP",
    Convergencia="SlowConv",
    Type_conv="Tight",
)


def generar(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    OrcaWork.generar(**DATOS, dir_principal="salida/", fecha=FECHA)
    return tmp_path / "salida" / "prueba" / "MnAl_2020_11_02"


def test_los_archivos_son_identicos_a_los_del_script_original(tmp_path, monkeypatch):
    # tests/golden se generó con la versión original del script, antes de reorganizarlo.
    carpeta = generar(tmp_path, monkeypatch) / "MnAl_proof_1"

    assert (carpeta / "job_slurm.sh").read_text() == (GOLDEN / "job_slurm.sh").read_text()
    assert (carpeta / "prueba.inp").read_text() == (GOLDEN / "prueba.inp").read_text()


def test_se_genera_una_carpeta_por_cada_base(tmp_path, monkeypatch):
    raiz = generar(tmp_path, monkeypatch)

    assert len(list(raiz.glob("MnAl_proof_*"))) == len(OrcaWork.Bases)


def test_la_primera_base_tambien_se_simula(tmp_path, monkeypatch):
    raiz = generar(tmp_path, monkeypatch)

    entrada = (raiz / "MnAl_proof_0" / "prueba.inp").read_text()

    assert entrada.startswith(f"! B3LYP SlowConv {OrcaWork.Bases[0]} \n")


def test_cada_carpeta_usa_la_base_de_su_numero(tmp_path, monkeypatch):
    raiz = generar(tmp_path, monkeypatch)

    entrada = (raiz / "MnAl_proof_96" / "prueba.inp").read_text()

    assert entrada.startswith(f"! B3LYP SlowConv {OrcaWork.Bases[96]} \n")
