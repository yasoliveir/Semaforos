import multiprocessing
import random
import time

colocacao = None
lock_colocacao = None


def init(cheg, lk):
    global colocacao, lock_colocacao
    colocacao = cheg
    lock_colocacao = lk


def sapo_correndo(id_sapo):
    global colocacao, lock_colocacao
    distancia_total = 50  # 50 cm para a linha de chegada
    distancia_percorrida = 0
    salto_max = 5  # tamanho máximo do salto em cm

    print(f"Sapo #{id_sapo} largou na corrida!")

    while distancia_percorrida < distancia_total:
        salto = random.randint(1, salto_max)
        distancia_percorrida += salto

        if distancia_percorrida > distancia_total:
            distancia_percorrida = distancia_total

        print(
            f"Sapo #{id_sapo} deu um salto de {salto}cm. Total percorrido: {distancia_percorrida}cm"
        )
        time.sleep(0.5)

    # Seção crítica protegida pelo Lock para definir a colocação corretamente
    with lock_colocacao:
        colocacao.value += 1
        posicao = colocacao.value

    print(f">>> Sapo #{id_sapo} chegou ao final na {posicao}ª posição! <<<")


def main():
    with multiprocessing.Manager() as gerenciador:
        cheg = gerenciador.Value("i", 0)  # Contador compartilhado para o pódio
        lk = gerenciador.Lock()  # Lock para proteger o incremento da colocação

        # Usando Pool com initializer para injetar as variáveis globais
        with multiprocessing.Pool(
            processes=5, initializer=init, initargs=(cheg, lk)
        ) as pool:
            # Lista com o ID dos 5 sapos
            sapatos = [1, 2, 3, 4, 5]
            pool.map(sapo_correndo, sapatos)

    print("\nFim da Corrida de Sapos!")


if __name__ == "__main__":
    main()