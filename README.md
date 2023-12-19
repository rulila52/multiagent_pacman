# Мультиагентный пакман

## Оглавление

* [О проекте](#о-проекте)
* [Команды для запуска](#команды-для-запуска)
* [Улучшения](#улучшения)
    * [Вопрос 1. Улучшить логику поведения ReflexAgent](#вопрос-1-улучшить-логику-поведения-reflexagent)

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