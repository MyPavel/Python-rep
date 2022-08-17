from django import template


register = template.Library()

F_WORDS = ['вакуум', 'вакуума', 'Цыгане', 'цыганского']


@register.filter()
def censor(in_text):
   for word in in_text.split():
      if word.lower() in F_WORDS:
         in_text = in_text.replace(
            word,
            f'{word[0]}{"*" * (len(word) - 1)}'
         )
   return in_text