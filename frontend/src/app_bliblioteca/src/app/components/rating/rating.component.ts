import { Component, Input, OnChanges, SimpleChanges } from '@angular/core';

@Component({
  selector: 'app-rating',
  templateUrl: './rating.component.html',
  styleUrl: './rating.component.css'
})
export class RatingComponent implements OnChanges{
  @Input() valor: number = 0;
  stars: boolean[] = [];

  ngOnChanges(): void {
      const round = Math.round(this.valor);
      this.stars = Array.from({length: 5}, (_, i) => i < round);
  }

}
