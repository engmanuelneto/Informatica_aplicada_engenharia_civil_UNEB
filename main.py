import re
import unicodedata
from cadastro import CadastroEstrutural
from elementos import Laje, Pilar, Viga


def contar_letras_limpas(texto: str) -> int:
    """Remove acentos, espaços e hífens e retorna a quantidade de letras."""
    sem_acento = unicodedata.normalize("NFD", texto)
    sem_acento = "".join(ch for ch in sem_acento if unicodedata.category(ch) != "Mn")
    apenas_letras = re.sub(r"[^A-Za-z]", "", sem_acento)
    return len(apenas_letras)


def main() -> None:
    nome_completo = "Manuel Aniceto Pereira Neto"
    partes_nome = nome_completo.split()

    primeiro_nome = partes_nome[0]
    ultimo_sobrenome = partes_nome[-1]

    n_letras = contar_letras_limpas(primeiro_nome)   # Manuel -> N = 6
    s_letras = contar_letras_limpas(ultimo_sobrenome)  # Neto -> S = 4

    # Parâmetros numéricos derivados de N e S (conforme regra da atividade)
    comprimento_base_m = 4.0 + (n_letras % 5) * 0.5            # 4.0 + (6 % 5)*0.5 = 4.5 m
    altura_base_m = 2.8 + ((n_letras + s_letras) % 5) * 0.2   # 2.8 + ((6+4) % 5)*0.2 = 2.8 m

    print(f"Estudante: {nome_completo}")
    print(f"N (letras de '{primeiro_nome}'): {n_letras} | S (letras de '{ultimo_sobrenome}'): {s_letras}")
    print(f"Parâmetros calculados -> comprimento_base_m: {comprimento_base_m:.2f} m | altura_base_m: {altura_base_m:.2f} m\n")

    cadastro = CadastroEstrutural(responsavel=nome_completo)

    pilar_01 = Pilar(
        identificacao="PILAR_MANUEL_01",
        pavimento="Térreo",
        fck_mpa=30.0,
        altura_m=altura_base_m,
        largura_b_m=0.30,
        profundidade_h_m=0.40,
        carga_axial_kn=850.0,
    )

    viga_02 = Viga(
        identificacao="VIGA_MANUEL_02",
        pavimento="1º Pavimento",
        fck_mpa=30.0,
        vao_m=comprimento_base_m,
        largura_bw_m=0.20,
        altura_h_m=0.50,
        carga_distribuida_kn_m=24.0,
    )

    laje_03 = Laje(
        identificacao="LAJE_MANUEL_03",
        pavimento="1º Pavimento",
        fck_mpa=25.0,
        comprimento_lx_m=comprimento_base_m,
        largura_ly_m=3.60,
        espessura_h_m=0.12,
    )

    cadastro.adicionar(pilar_01)
    cadastro.adicionar(viga_02)
    cadastro.adicionar(laje_03)

    cadastro.listar_resumo()
    cadastro.exibir_detalhes()

    print("-" * 60)
    print(f"Volume total de concreto: {cadastro.volume_total_m3():.4f} m³")
    print(f"Peso próprio total estimado: {cadastro.peso_proprio_total_kn():.2f} kN")


if __name__ == "__main__":
    main()