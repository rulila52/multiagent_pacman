# Мультиагентный пакман

Ультрасупермегаумный агент для игры в Пакмана (возможно)

## Оглавление

* [О проекте](#о-проекте)
* [Команды для запуска](#команды-для-запуска)
* [Улучшения](#улучшения)
    * [Вопрос 1. Улучшить логику поведения ReflexAgent](#вопрос-1-улучшить-логику-поведения-reflexagent)
    * [Вопрос 2. Реализовать алгоритм MinimaxAgent через оценку дерева игры](#вопрос-2-реализовать-алгоритм-minimaxagent-через-оценку-дерева-игры)
    * [Вопрос 3. Создать агента AlphaBetaAgent](#вопрос-3-создать-агента-alphabetaagent)
    * [Вопрос 4. Создать агента ExpectimaxAgent](#вопрос-4-создать-агента-expectimaxagent)
    * [Вопрос 5. Написать функцию оценки лучше представленной](#вопрос-5-написать-функцию-оценки-лучше-представленной)
    * [Дополнительный вопрос. Написать своего агента](#дополнительный-вопрос-написать-своего-агента)

## О проекте

Данный проект посвящен реализации различной логики поведения Пак-Мана. 
За основу взят проект с этого 
[сайта](https://www.cs.utexas.edu/~pstone/Courses/343spring10/assignments/multiagent/multiagentProject.html),
задания описаны подробнее там же.

## Команды для запуска

```python pacman.py```

```python pacman.py -p ReflexAgent```

```python pacman.py -p ReflexAgent -l testClassic```

```python pacman.py --frameTime 0 -p ReflexAgent -k 1```

```python pacman.py --frameTime 0 -p ReflexAgent -k 2```

```python pacman.py -p ReflexAgent -l openClassic -n 10 -q```

```python pacman.py -p MinimaxAgent -l minimaxClassic -a depth=4```

```python pacman.py -p MinimaxAgent -l trappedClassic -a depth=3```

```python pacman.py -p AlphaBetaAgent -a depth=3 -l smallClassic```

```python pacman.py -p AlphaBetaAgent -l trappedClassic -a depth=3 -q -n 10```

```python pacman.py -p ExpectimaxAgent -l trappedClassic -a depth=3 -q -n 10```

```python pacman.py -l smallClassic -p ExpectimaxAgent -a evalFn=better -q -n 10```

```python pacman.py -l contestClassic -p ContestAgent -g DirectionalGhost -q -n 10```

## Улучшения

### Вопрос 1. Улучшить логику поведения ReflexAgent

### Описание

Улучшите ReflexAgent в multiAgents.py, чтобы играть достойно. Приведенный код 
рефлекс-агента содержит несколько полезных примеров методов, которые запрашивают 
информацию у GameState. Способному рефлекторному агенту придется учитывать как 
места с едой, так и места с призраками, чтобы работать хорошо.

### Описание улучшения

[Посмотреть реализацию.](https://github.com/rulila52/multiagent_pacman/blob/master/multiAgents.py#L17-L86)
Теперь он учитывает текущую ситуацию на поле. Не смотрит надолго вперед, 
оценивает текущую ситуацию на поле. Довольно часто побеждает, но возникают 
простои из-за анализа только текущей ситуации.

### Результаты тестов

На макете testClassic, 10 тестов 
(`python pacman.py -p ReflexAgent -l testClassic`):

```
Pacman emerges victorious! Score: 557
Pacman emerges victorious! Score: 553
Pacman emerges victorious! Score: 563
Pacman died! Score: -498
Pacman emerges victorious! Score: 561
Pacman emerges victorious! Score: 549
Pacman emerges victorious! Score: 545
Pacman emerges victorious! Score: 547
Pacman emerges victorious! Score: 561
Pacman emerges victorious! Score: 553
```

На макете mediumClassic с 1-им призраком, 5 тестов 
(`python pacman.py --frameTime 0 -p ReflexAgent -k 1`):

```
Pacman emerges victorious! Score: 1220
Pacman died! Score: 343
Pacman emerges victorious! Score: 1184
Pacman emerges victorious! Score: 1190
Pacman emerges victorious! Score: 1254
```

На макете mediumClassic с 2-мя призраками, 5 тестов
(`python pacman.py --frameTime 0 -p ReflexAgent -k 2`):

```
Pacman emerges victorious! Score: 1729
Pacman emerges victorious! Score: 1863
Pacman emerges victorious! Score: 1429
Pacman died! Score: 197
Pacman emerges victorious! Score: 1300
```

### Вопрос 2. Реализовать алгоритм MinimaxAgent через оценку дерева игры

### Описание

Написать состязательный поисковый агент в предоставленной заглушке класса 
MinimaxAgent в multiAgents.py. Ваш минимакс-агент должен работать с любым 
количеством призраков, поэтому вам придется написать алгоритм, который будет 
немного более общим, чем тот, который представлен в учебнике. В частности, 
ваше минимакс-дерево будет иметь несколько минимальных слоев (по одному для 
каждого призрака) для каждого максимального слоя. Обратите внимание, что игра 
развивается по круговому принципу: pacman делает шаг, затем Ghost1 делает шаг, 
затем Ghost2 делает шаг..., затем pacman делает шаг и так далее.

### Описание улучшения

[Посмотреть реализацию.](https://github.com/rulila52/multiagent_pacman/blob/748643d7d7a728076d14ce15fd400972d62cf775/multiAgents.py#L108-L129)
Алгоритм осуществляет поиск в глубину по дереву игры. На каждом уровне дерева 
сменяются Max и Min, исходя из текущего игрового состояния. Листья дерева 
оцениваются при помощи функции оценки (evaluation function). Алгоритм рекурсивно 
распространяется вверх по дереву, принимая решения в каждом узле для максимизатора
(пакман) и минимизатора (призраки). В конечном итоге алгоритм принимает решение 
о следующем шаге, выбирая действие, которое приведет к максимальному 
(или минимальному) ожидаемому выигрышу.

Когда Пакман считает, что его смерть неизбежна, он постарается закончить игру 
как можно скорее из-за постоянного штрафа за выживание. Иногда это неправильно 
поступать со случайными призраками, но минимаксные агенты всегда предполагают худшее.

Большая глубина дерева обеспечивает прекрасные результаты, но при увеличении карты 
алгоритм с большой глубиной дерева будет выполняться очень долго и будет зависать.

### Результаты тестов

На макете minimaxClassic с глубиной 8, 10 тестов
(`python pacman.py -p MinimaxAgent -l minimaxClassic -a depth=8`):

```
Pacman emerges victorious! Score: 516
Pacman emerges victorious! Score: 516
Pacman emerges victorious! Score: 516
Pacman died! Score: -493
Pacman emerges victorious! Score: 516
Pacman emerges victorious! Score: 516
Pacman died! Score: -493
Pacman emerges victorious! Score: 516
Pacman emerges victorious! Score: 516
Pacman emerges victorious! Score: 516
```

## Вопрос 3. Создать агента AlphaBetaAgent

### Описание

Создать в AlphaBetaAgent новый агент, который использует обрезку альфа-бета 
для более эффективного исследования минимаксного дерева.

### Описание улучшения

[Посмотреть реализацию.](https://github.com/rulila52/multiagent_pacman/blob/748643d7d7a728076d14ce15fd400972d62cf775/multiAgents.py#L131-L177)
Альфа-бета отсечение — это оптимизация алгоритма минимакса, предназначенная 
для уменьшения количества рассматриваемых узлов в дереве игры. Алгоритм 
использует два параметра, называемых "альфа" и "бета", чтобы уменьшить 
диапазон значений, которые нужно рассматривать в узлах дерева.

Данный алгоритм считает, что призраки всегда ходят оптимально для себя, но
в реальности это не так, поэтому этот алгоритм подходит далеко не во всех случаях.

### Результаты тестов

На макете minimaxClassic с глубиной 8, 10 тестов
(`python pacman.py -p AlphaBetaAgent -l minimaxClassic -a depth=8`):

```
Pacman emerges victorious! Score: 516
Pacman emerges victorious! Score: 516
Pacman died! Score: -493
Pacman emerges victorious! Score: 516
Pacman emerges victorious! Score: 506
Pacman emerges victorious! Score: 516
Pacman emerges victorious! Score: 516
Pacman died! Score: -497
Pacman emerges victorious! Score: 516
Pacman emerges victorious! Score: 516
```

## Вопрос 4. Создать агента ExpectimaxAgent

### Описание

Создать ExpectimaxAgent, где ваш агент-агент больше не будет принимать 
минимальное значение для всех действий призраков, а будет ожидать в соответствии 
с моделью вашего агента того, как действуют призраки.

### Описание улучшения

[Посмотреть реализацию.](https://github.com/rulila52/multiagent_pacman/blob/748643d7d7a728076d14ce15fd400972d62cf775/multiAgents.py#L179-L196)
Вместо того чтобы минимизировать по всем возможным ходам оппонента (как в Minimax), 
мы усредняем результаты, учитывая вероятности каждого хода оппонента. Вероятности 
вычисляются с учетом предположения о стратегии оппонента.

Для ExpectimaxAgent мы предполагаем, что призраки действуют случайным образом. 
Мы вычисляем ожидаемое значение для хода призраков, усредняя значения для всех 
их возможных ходов с равными вероятностями.

Слой Max (Pacman): В этом слое Pacman выбирает ход, который максимизирует его 
ожидаемую выгоду. Мы используем max, чтобы выбрать наилучший ход.

Слой Expectation (Призраки): В этом слое мы усредняем результаты для каждого 
возможного хода призрака с равными вероятностями. Это отражает предположение, 
что призраки действуют случайным образом.

### Результаты тестов и сравнение ExpectimaxAgent с AlphaBetaAgent

`python pacman.py -p AlphaBetaAgent -l trappedClassic -a depth=8 -q -n 10`

```
Pacman died! Score: -501
Pacman died! Score: -501
Pacman died! Score: -501
Pacman died! Score: -501
Pacman died! Score: -501
Pacman died! Score: -501
Pacman died! Score: -501
Pacman died! Score: -501
Pacman died! Score: -501
Pacman died! Score: -501
Average Score: -501.0
Scores:        -501, -501, -501, -501, -501, -501, -501, -501, -501, -501
Win Rate:      0/10 (0.00)
Record:        Loss, Loss, Loss, Loss, Loss, Loss, Loss, Loss, Loss, Loss
```

`python pacman.py -p ExpectimaxAgent -l trappedClassic -a depth=8 -q -n 10`

```
Pacman emerges victorious! Score: 532
Pacman emerges victorious! Score: 532
Pacman died! Score: -502
Pacman died! Score: -502
Average Score: 15.0
Scores:        532, -502, 532, 532, 532, -502, -502, 532, -502, -502
Win Rate:      5/10 (0.50)
Record:        Win, Loss, Win, Win, Win, Loss, Loss, Win, Loss, Loss
```

На карте с ловушкой ExpectimaxAgent действует лучше, в то время как 
AlphaBetaAgent всегда проигрывает, потому что считает, что призраки 
ходят наилучшим образом, и сдается.

## Вопрос 5. Написать функцию оценки лучше представленной

### Описание

Напишите лучшую функцию оценки для pacman в предоставленной функции 
BetterEvaluationFunction. Функция оценки должна оценивать состояния, 
а не действия, как это делала ваша функция оценки рефлекторного агента. 
Для оценки вы можете использовать любые имеющиеся в вашем распоряжении 
инструменты, включая код поиска из последнего проекта.

### Описание улучшения

[Посмотреть реализацию.](https://github.com/rulila52/multiagent_pacman/blob/748643d7d7a728076d14ce15fd400972d62cf775/multiAgents.py#L198-L222)

Новая функция оценки учитывает следующие аспекты:

- Текущий счет: Мы хотим максимизировать текущий счет.
- Ближайший призрак: Мы хотим минимизировать расстояние до ближайшего призрака.
- Ближайшая еда: Мы хотим минимизировать расстояние до ближайшей еды.

Эти компоненты оценки позволяют Пакману избегать призраков, приближаться к еде 
и максимизировать свой счет.

### Результаты тестов

`python pacman.py -l smallClassic -p ExpectimaxAgent -a evalFn=better -q -n 100`

```
Average Score: 407.893
Average Win Score: 930.7966101694915
Average Lose Score: -184.136460554371
Win Rate:      531/1000 (0.53)
```

## Дополнительный вопрос. Написать своего агента

### Описание

В данном разделе я поставил себе более простую цель - написать агента, который улучшит 
результаты предыдущего. 

### Описание улучшения

[Посмотреть реализацию.](https://github.com/rulila52/multiagent_pacman/blob/748643d7d7a728076d14ce15fd400972d62cf775/multiAgents.py#L227-L319)
Новый агент является модернизацией алгоритма ExpectimaxAgent, но с проверкой, 
не окружен ли пакман призраками, применяем стратегиями избегания призраков, 
приближения к капсулам, предпочтения дорог с едой и избегания тупиков.

### Результаты тестов

`python pacman.py -l smallClassic -p ContestAgent -a evalFn=better -q -n 1000`

```
Average Score: 475.421
Average Win Score: 924.139802631579
Average Lose Score: -220.55102040816325
Win Rate:      608/1000 (0.61)
```